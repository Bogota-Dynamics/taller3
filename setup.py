from setuptools import setup

package_name = 'taller3'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sebastian',
    maintainer_email='s.guerrero3@uniandes.edu.co',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = taller3.robot_manipulador_teleop:main',
            'listener = taller3.robot_manipulador_control:main',
            'pos = taller3.robot_manipulador_pos:main',
            'interfaz = taller3.robot_manipulador_interfaz:main',
            'planner = taller3.robot_manipulador_planner:main',
        ],
    },
)
