require('devtools')

# manual installation
chooseCRANmirror(graphics=FALSE, ind=1)
install.packages('rgdal', type = "source", 
                    configure.args=c('--with-proj-include=/usr/local/include', '--with-proj-lib=/usr/local/lib'))

devtools::install_github('e-sensing/sits')
devtools::install_github("e-sensing/inSitu")
