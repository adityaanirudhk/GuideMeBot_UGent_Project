from setuptools import setup
import os
from glob import glob

package_name = 'guide_me_bot'

data_files = [
    ('share/ament_index/resource_index/packages', [
        'resource/guide_me_bot',
    ]),
    ('share/guide_me_bot', ['package.xml']),
    (os.path.join('share', 'guide_me_bot', 'launch'), glob('launch/*.launch.py')),
    (os.path.join('share', 'guide_me_bot', 'config'), glob('config/*.yaml')),
    (os.path.join('share', 'guide_me_bot', 'maps'), glob('maps/*')),
]

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Noah Delvoye, Aditya Kakarlamudi, Tybo Verslype, Joseph Thompson',
    maintainer_email='noah.delvoye@ugent.be, aditya.kakarlamudi@ugent.be, tybo.verslype@ugent.be, joseph.thompson@ugent.be',
    description='Autonomous indoor navigation and guiding robot: GuideMeBot (Group 3)',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'conversation_manager = guide_me_bot.conversation_manager:main',
            'speech_handler = guide_me_bot.speech_handler:main',
            'whisper_bridge = guide_me_bot.whisper_bridge:main',
            'gui_navigator = guide_me_bot.gui_navigator:main',
        ],
    },
)
