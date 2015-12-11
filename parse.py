def parse(command,allcommands):
	allcommands.sort()
	results = []
	if command == "":
		return results
	command = command.strip()
	for c in allcommands:
		if "".join([x[0] for x in c.split(" ")])==command:
			if not c in results:
				results.append(c)
	for c in allcommands:
		if c.startswith(command):
			if not c in results:
				results.append(c)
				
	for c in allcommands:		
		if (not False in [c.split(" ")[min(i,len(c.split(" "))-1)].startswith(command.split(" ")[i]) for i in range (len(command.split(" ")))]):
			if not c in results:
				results.append(c)					
	for c in allcommands:
		if "".join(c.split(" ")).startswith(command):
			if not c in results:
				results.append(c)				
	for c in allcommands:
		if "".join([x[0] for x in c.split(" ")]).startswith(command):
			if not c in results:
				results.append(c)
	for c in allcommands:
		for d in c.split(" "):
			if d.startswith(command):
				if not c in results:
					results.append(c)
	for c in allcommands:
		if command in "".join(c.split(" ")[i][0] for i in range(0,len(c.split(" ")))):
			if not c in results:
				results.append(c)
	
	return results
if __name__ == "__main__":
	while 1:
		print(parse(raw_input("?"),[
		"kill horse","kill dog","khan","kill cat","open door","eat meat","restore full health","roast full chicken","raw fury","eat shit","eat mother","kill motherfucker"]))
