import yaml
import itertools
import os
from configparser import ConfigParser

def get_subnet_base_ip(subnet):
    # Extract the base IP from a subnet string (e.g., "172.23.0.0/16" -> "172.23")
    return '.'.join(subnet.split('.')[:2])

def get_subnet_third_octet(subnet):
    # This assumes a /16 subnet and provides an initial value for the third octet
    base_ip = get_subnet_base_ip(subnet)
    return f"{base_ip}.0"

def increment_ip(ip):
    # Increment the last octet of the IP address
    parts = ip.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)

def generate_networks_config(sections, config):
    networks = {}
    for section in sections:
        ip_address = config[section]['IPv4_address']
        network_name = f"{section}_network"
        networks[network_name] = {
            'ipam': {
                'config': [{'subnet': ip_address}]
            }
        }
    return networks

def generate_services_config(config, start_port):
    services = {}
    application_port = 5001

    sections = config.sections()
    # All possible pairs of sections for relay containers
    section_pairs = list(itertools.combinations(sections, 2))

    # To ensure unique IP addresses for relay containers
    ip_tracker = {}

    for section in sections:
        network_name = f"{section}_network"
        if 'num_satellite' in config[section]:
            satellite_count = int(config[section]['num_satellite'])
            subnet = config[section]['IPv4_address']
            subnet_base_ip = get_subnet_base_ip(subnet)
            subnet_third_octet_start = 1  # Initialize the third octet

            for i in range(satellite_count):
                service_name = f"{section}_{i+1}"
                ip_address = f"{subnet_base_ip}.{subnet_third_octet_start + i}.{2}"
                services[service_name] = {
                    'build': {
                        'context': './',
                        'dockerfile': './input/Dockerfile'
                    },
                    'container_name': service_name,
                    'networks': {
                        network_name: {'ipv4_address': ip_address}
                    },
                    'ports': [f"{start_port}:{application_port}"],
                    'tty': True,
                    'privileged': True
                }
                start_port += 1
        else:
            raise ValueError(f"The section '{section}' does not contain the 'num_satellite' key.")

    for pair in section_pairs:
        relay_name = f"relay_{'_'.join(pair)}"
        subnet1 = config[pair[0]]['IPv4_address']
        subnet2 = config[pair[1]]['IPv4_address']

        subnet1_base_ip = get_subnet_base_ip(subnet1)
        subnet2_base_ip = get_subnet_base_ip(subnet2)

        ip_address1 = ip_tracker.get(pair[0], f"{subnet1_base_ip}.0.2")
        ip_address2 = ip_tracker.get(pair[1], f"{subnet2_base_ip}.0.2")
        
        services[relay_name] = {
            'build': {
                'context': './',
                'dockerfile': './input/Dockerfile'
            },
            'container_name': relay_name,
            'networks': {
                f"{pair[0]}_network": {'ipv4_address': ip_address1},
                f"{pair[1]}_network": {'ipv4_address': ip_address2}
            },
            'ports': [f"{start_port}:{application_port}"],
            'tty': True,
            'privileged': True
        }
        start_port += 1
        
        # Update IP tracker to ensure the next relay for these networks gets a different IP
        ip_tracker[pair[0]] = increment_ip(ip_address1)
        ip_tracker[pair[1]] = increment_ip(ip_address2)

    return services

def generate_docker_compose(config):
    start_port = 50000 # Host port number to start with
    networks = generate_networks_config(config.sections(), config)
    services = generate_services_config(config, start_port)

    return {
        'version': '3',  # Specify the Docker Compose file version
        'services': services,
        'networks': networks
    }

def main():
    config = ConfigParser()
    config.read(os.path.join('./input/', 'emulation.config'))

    docker_compose_data = generate_docker_compose(config)
    with open('docker-compose.yml', 'w') as file:
        yaml.dump(docker_compose_data, file, default_flow_style=False)

if __name__ == '__main__':
    main()