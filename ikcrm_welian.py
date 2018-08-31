#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging

# it should be set on a config file, I do not want to set now
logging.basicConfig(level = logging.INFO,
                    format = '%(message)s'
)

from ikcrmManager import ikcrmSignIn
from ikcrmManager import ikcrmSearchInfo


if __name__ == '__main__':

    
    isCookieExists = (os.path.exists('mozilla_cookie.txt'))

    if isCookieExists is False:
        login = ikcrmSignIn('IKCRM SIGN IN', 'IKCRM账户手机号')
        login.run()
        logging.debug('login over')

    isCookieExists = (os.path.exists('mozilla_cookie.txt'))
    if isCookieExists is True:
        check = ikcrmSearchInfo()
        check.run()
        logging.debug('check over')

    sys.exit()




