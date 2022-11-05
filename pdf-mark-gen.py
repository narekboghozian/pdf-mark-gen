import sys
import os
import pprint

# To-do
# - Integrate roman numerals pages somehow
# - Add tab for txt type docs


# How to use
# Example command: 
# gs -o <path to out> -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress <path to pdf>  <pdfmarks file>
# 

def open_spec(filename):
	lines = []
	try:
		lines = open(filename, 'r').read().splitlines()
	except FileNotFoundError:
		print("Spec file '%s' not found"%(filename))
	return lines

def decode_spec(raw_spec):

	
	processed_spec = {"invalid":[], "warning":[], "content":[]}
	commands = ["offset"]
	character_swaps = [["–","-"],["’","'"]]

	invalid = []
	warning = []

	tabs = []
	special = []
	titles = []

	page = 0
	tabs = 0
	offset = 0

	for i, raw_line in enumerate(raw_spec):
		processed_line = {}
		if len(raw_line) >= 2:

			# print(raw_line)
			line = raw_line.split()

			if line[0] in commands:
				page = int(line[1])
				offset = page - int(line[2])
				# print("Offset = " + str(offset))
				if len(line) >= 5:
					warning.append(line)

			else:
				numStart = raw_line.strip().rfind('.') + 1
				page = int(raw_line.strip()[numStart:].split()[0])
				line = raw_line.strip()[:numStart].split()
				line = raw_line.strip()[:numStart]
				for i, letter in enumerate(line[::-1]):
					if (letter != '.') and (letter != ' '):
						titleEnd = numStart - i
						break


				title = raw_line.strip()[:titleEnd].strip()
				for char in character_swaps:
					title = title.replace(char[0], char[1])

				tabs = raw_line.split(' ')[0].count('\t')

				processed_line["page"]  = page + offset
				processed_line["title"] = title
				processed_line["tabs"] = tabs
				# print("%s, tabs= %d"%(title, tabs))
				processed_spec["content"].append(processed_line)
		
		else:
			invalid.append(raw_line)

	
	for i, line in enumerate(processed_spec["content"][0:-1]):

		dist  = len(processed_spec["content"])
		count = 0
		cur_tab = line["tabs"]

		for j in range(i+1, dist):
			nex_tabs = processed_spec["content"][j]["tabs"]
			if nex_tabs == cur_tab + 1:
				count += 1
			elif nex_tabs == cur_tab:
				break

		processed_spec["content"][i]["count"] = str(-count)
	processed_spec["content"][-1]["count"] = str(0)

	processed_spec["invalid"] = invalid
	processed_spec["warning"] = warning
	return processed_spec

def format_marks(proc_spec):
	formatted_spec = []
	for item in proc_spec["content"]:
		line = '[ /Page %s /Count %s /Title (%s) /OUT pdfmark'%(
				item["page"],
				item["count"],
				item['title']
				)
		# print(line)
		formatted_spec.append(line)
	return formatted_spec

def save_spec(formatted_spec, path, name):
	status = False
	try:
		fullpath = os.path.join(path, name)
		exists = os.listdir(path)
		choice = 'y'
		yes = ['y','yes']
		no = ['no','n']
		options = yes + no

		if name in exists:
			print("File: '%s' already exists in '%s/'"%(name, path))
			choice = input('Type "y/n" to overwrite or abort: ').lower()
			
			while choice not in options:
				print('"%s" is not a valid option'%(choice))
				choice = input('Type "y" to overwrite or "n" abort: ').lower()

		if choice in yes:
			with open(fullpath, 'w+', encoding='utf-8') as f:
				for line in formatted_spec:
					f.write(line)
					f.write('\n')
			status = True

		elif choice in no:
			print("File: '%s' not written"%(name))
			
	except FileNotFoundError:
		print("No such directory: '%s'"%(path))
	return {"fullpath":fullpath, "status":status, "name":name}

def print_help():
	print("")
	print("pdfmarkgen v0.2\n")
	print("Usage:")
	print("pdfmarkgen 'full/path/to/input/file' 'other files...' 'however many you want...' \n\n")
	print("Using gs to apply pdfmarks:\n")
	print("gs -o <path to out> -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress <path to pdf>  <pdfmarks file>\n\n")

def main():
	pp = pprint.PrettyPrinter(width=120)
	numArgs = len(sys.argv)
	args = sys.argv[1:]
	help_cmds = ['-h','-help','--h','--help']
	if any(arg in help_cmds for arg in args) or (len(args) == 0):
		print_help()
	else:
		for ind, arg in enumerate(args):
			raw_spec = open_spec(arg)
			proc_spec = decode_spec(raw_spec)
			formatted_spec = format_marks(proc_spec)
			filename = "pdfmarks_%s"%(arg.split('/')[-1])
			savepath = '/'.join(arg.split('/')[:-1])
			ret = save_spec(formatted_spec, savepath, filename)
			if ret['status']:
				print("Saved marks for %s as %s"%(arg, ret["name"]))
				gs_stuff = ('OUT_%s.pdf'%(ind),'IN_%s.pdf'%(ind), ret['fullpath'].replace(' ','\\ '))
				print("\nTo apply to file, use:")
				print("gs -o %s\\\n -sDEVICE=pdfwrite \\\n -dPDFSETTINGS=/prepress \\\n %s \\\n %s\n\n"%gs_stuff)


if __name__ == '__main__':
	main()











