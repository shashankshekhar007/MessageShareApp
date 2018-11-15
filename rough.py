	try:
		option = clientsocket.myreceive()
    except Exception as e:
	    raise e
    if option == '0':
	  	try:
			clientsocket.mysend('Enter \n[0] HELP \n[1] List Files\n[2] Upload File\n[3] Download File \n[4] Delete File\n[5] Give Access\n[6] Revoke Access\n[7] Shared Files\n[8] Exit\n')
	    except Exception as e:
			raise e
    if option == '1':
	    try:
			clientsocket.mysend(curruser.ls()+'\nShared Files: \n'+curruser.shared_to_me())
	    except Exception as e:
			raise e

    if option == '2':      
	    try:
			filename = clientsocket.myreceive()
	    except Exception as e:
			raise e
	    if filename =='#####----#####':
			continue
	    try:
			clientsocket.mysend("Transferring File............\n")
	    except Exception as e:
			raise e
	  	try:
			filedata = clientsocket.myreceive()
	    except Exception as e:
			raise e
	    curruser.writefile(filename, filedata)

    if option == '3':      
	    try:
			filename = clientsocket.myreceive()
	    except Exception as e:
			raise e
	    print("Going to see the file now")
	    filedata = curruser.readfile(filename)
	    print("Seen the file")
	    print(filedata)
	    if "File doesn't exist!!\n" == filedata:
			filedata = curruser.shared_read(filename)
			if "File is not shared with you!!\n" == filedata:
				try:
					clientsocket.mysend("File doesn't exist!!\n")
				except Exception as e:
					raise e
		 	else:
				try:
			   		clientsocket.mysend(filedata)
				except Exception as e:
			   		raise e
	    else:
			try:
				clientsocket.mysend(filedata)
	    	except Exception as e:
				raise e
    if option == '4':
		try:
			clientsocket.mysend("Enter File Name\n")
	    except Exception as e:
			raise e
	    try:
			filename = clientsocket.myreceive()
	  	except Exception as e:
			raise e
	  	delete_msg = curruser.deletefile(filename)
	  	try:
			clientsocket.mysend(delete_msg)
	    except Exception as e:
			raise e
    if option == '5':
	  	try:
			clientsocket.mysend("Enter Filename:Username\n")
	    except Exception as e:
			raise e
	  	try:
			l = clientsocket.myreceive().strip('\n').split(':')
	  	except Exception as e:
			raise e
	  	msg = curruser.shareit(l[0],l[1])
	  	try:
			clientsocket.mysend(msg)
	  	except Exception as e:
			raise e
    
    if option == '6':
	  	try:
			clientsocket.mysend("Enter Filename:Username\n")
	  	except Exception as e:
			raise e
	    try:
			l = clientsocket.myreceive().strip('\n').split(':')
	  	except Exception as e:
			raise e
	    msg = curruser.takeback(l[0],l[1])
	  	try:
			clientsocket.mysend(msg)
	  	except Exception as e:
			raise e

    if option == '7':
		try:
			clientsocket.mysend(curruser.i_shared())
	  	except Exception as e:
			raise e

    if option == '8':
		try:
			clientsocket.mysend("Closing Connection...\n")
	    except Exception as e:
			raise e
		return