from setuptools import setup, find_packages

setup(
    name='certbot-dns-varo',
    version='0.1.0',
    description='Certbot plugin for Varo',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'certbot>=1.1.0',
        'requests',
        'zope.interface',
    ],
    entry_points={
        'certbot.plugins': [
            'dns-varo = certbot_dns_varo.dns_varo:Authenticator',
        ],
    },
)
