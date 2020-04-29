

def downloadURL (filepath, URL):
    # download URL and store to Local path as a general binary file

    # python library urllib is used

    # def downloadURL (filepath, URL):

    '''Function to download URL'''

    from urllib import request #or import urllib.request
    import urllib.error

    #https://docs.python.org/3.1/howto/urllib2.html

    #function from urllib to download file
    webRequest = urllib.request.Request(URL)

    #need to make sure our code doesnt run if URL is broken so we use TRY and EXCEPT

    try:
        page=urllib.request.urlopen(webRequest) #downloads the URL

        #use page.read to read the contents

        contents = page.read()     #the .read() executes the read function from the "page" program

        #the below with condition ensures only runs when the file correctly opens
        #its another fail safe
        with open(filepath,"wb") as output: #thios with block closes file even if not explicitly said
            output.write(bytearray(contents))\
            #wb is the mode of opening ie binary contents
            #this ises the write function inh the output program and makes the contents output as a local filepath
            # as byte array so we are agnbostic to what file type we are downloading, eg zip or csv etc

    #now to write the except block, incase errors
    except urllib.error.URLError as e:  #error now classified as e variable
        #printing error
        print (e).fp.read()



