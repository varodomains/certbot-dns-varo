from setuptools import setup, find_packages

setup(
    name='certbot-dns-varo',
    version='1.0.0',
    description='A Certbot plugin for Varo',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/varodomains/certbot-dns-varo',
    author='eskimo',
    author_email='me@eskimo.dev',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'certbot',
        'requests',
        'zope.interface',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'certbot.plugins': [
            'dns-varo = certbot_dns_varo.dns_varo:Authenticator',
        ],
    },
)
