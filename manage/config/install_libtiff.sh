wget ftp://ftp.remotesensing.org/pub/libtiff/tiff-4.0.3.tar.gz

tar xvzf tiff-4.0.3.tar.gz
cd tiff-4.0.3/
./configure
make
sudo make install
cd ..
