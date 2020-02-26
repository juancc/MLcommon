from distutils.core import setup
setup(
  name = 'MLcommon',
  packages = ['MLcommon'],
  version = '0.1',
  license= '',
  description = 'Common interface for Machine Learning models with explicit model protocol',
  author = 'Juan Carlos Arbeláez',
  author_email = 'juanarbelaez@vaico.com.co',
  url = 'https://jarbest@bitbucket.org/jarbest/mlcommon.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['VAICO', 'COMMON', 'ML'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)