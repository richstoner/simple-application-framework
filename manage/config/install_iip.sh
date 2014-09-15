svn checkout svn://svn.code.sf.net/p/iipimage/code/ iipimage-code
cd iipimage-code
cd iipsrv
cd trunk
./autogen.sh
./configure --with-tiff-includes=/usr/local/include --with-tiff-libraries=/usr/local/lib
make
cd ..
cd ..
