
from setuptools import setup

setup(name='meshroombot',
      version='0.1.1',
      description='The funniest joke in the world',
      url='https://github.com/JesseLeeuwen/meshroombot.git',
      author='Jesse van Leeuwen',
      author_email='jesse@emberglitch.com',
      license='MIT',
      packages=['meshroombot'],
      scripts=['bin/meshroombot-run', 'bin/meshroombot-setup'],
      zip_safe=False)