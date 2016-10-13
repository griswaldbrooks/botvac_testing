from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='botvac_tools',
      version='0.3',
      description=('A package of utilities for developing'
                   'with the Neato Botvac.'),
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering',
        ],
      keywords='neato robotics botvac tools',
      url='http://github.com/griswaldbrooks/botvac_tools',
      author='Griswald Brooks',
      author_email='griswald.brooks@gmail.com',
      license='MIT',
      packages=['botvac_tools'],
      install_requires=[
        'argparse',
        'matplotlib',
        'numpy'
        ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
        'console_scripts': ['plot_scan=lds_tools.plot_scan:main'],
        },
      include_package_data=True,
      zip_safe=False)
