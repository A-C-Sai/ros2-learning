from setuptools import find_packages, setup
import os

package_name = 'py_publisher_subscriber'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sai C Akella',
    maintainer_email='sai.c.akella@gmail.com',
    description='minimal publisher/subscriber using rclpy',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher_member_function = py_publisher_subscriber.publisher_member_function:main',
            'subscriber_member_function = py_publisher_subscriber.subscriber_member_function:main',
        ],
    },
    scripts=['scripts/minimal_pub_sub_launch.sh'],
)
