import logging
from optparse import OptionParser
from sss import app

parser = OptionParser()
parser.add_option('-d', '--debug', dest='debug',
                  help='Run app in debug mode', action='store_true', default=False)

(options, args) = parser.parse_args()

if options.debug:
    print ' * Setting debug mode'
    app.config['DEBUG'] = True
    app.logger.setLevel(logging.ERROR)

app.run(host='0.0.0.0')
