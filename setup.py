from distutils.core import setup

setup(
    name = "pygtpnl",
    packages = ["pygtpnl"],
    version = "0.1",
    description = "Python wrapper to libgptnl",
    author = "Aapo Poutanen",
    author_email = "aapo.poutanen@cumucore.com",
    keywords = ["netlink", "gtp", "sgw"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        ]
)
