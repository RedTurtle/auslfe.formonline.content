from setuptools import setup, find_packages
import os

version = '0.8.1'

setup(name='auslfe.formonline.content',
      version=version,
      description="The Form Online content type for Plone",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='plonegov form plone',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/auslfe.formonline.pfgadapter',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['auslfe', 'auslfe.formonline'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
