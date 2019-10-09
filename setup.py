from distutils.core import setup

setup(
    name = "pygtpnl",
    packages = ["pygtpnl"],
    version = "0.2",
    description = "Python wrapper to libgptnl",
    author = "Aapo Poutanen",
    author_email = "aapo.poutanen@cumucore.com",
    url = "https://github.com/cumucore/pygtpnl",
    keywords = ["netlink", "gtp", "sgw"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: Linux",
        ]
)
