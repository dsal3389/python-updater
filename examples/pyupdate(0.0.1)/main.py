from pyupdate.UPDATE import UPDATE

def test1():
	print("test1")

if __name__ == '__main__':
	_update = UPDATE(__file__) # to update to current file
	_update.update_from_file('update.txt').update()
	# the update file dosent need to be .txt just a readable file
	test1()
