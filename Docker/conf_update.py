
import ConfingParser

path_cuckoo = "/cape/conf/cuckoo.conf"
conf_cuckoo = ConfingParser.ConfingParser()
conf_cuckoo.read(path_cuckoo)
with open(path_cuckoo, 'w') as conf:
	conf_cuckoo.set('resultserver', 'ip', '0.0.0.0')
	conf_cuckoo.set('resultserver', 'port', '2042')
	conf_cuckoo.set('cuckoo', 'machinery', 'virtualbox')

	conf_cuckoo.write(conf)
