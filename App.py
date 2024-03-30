from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import os
import base64, os

app = Flask(__name__)
app.secret_key = 'a'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ServerLogin')
def ServerLogin():
    return render_template('ServerLogin.html')


@app.route('/OwnerLogin')
def OwnerLogin():
    return render_template('OwnerLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewOwner')
def NewOwner():
    return render_template('NewOwner.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route('/TrapdoorLogin')
def TrapdoorLogin():
    return render_template('TrapdoorLogin.html')


@app.route("/tlogin", methods=['GET', 'POST'])
def tlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb ")
            data = cur.fetchall()
            return render_template('THome.html', data=data)

        else:
            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)


@app.route("/THome")
def THome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb")
    data = cur.fetchall()
    return render_template('THome.html', data=data)


@app.route("/FileInfo")
def FileInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb")
    data = cur.fetchall()
    return render_template('FileInfo.html', data=data)


@app.route("/TUserRequest")
def TUserRequest():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting'  ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status !='Accept'  ")
    data1 = cur.fetchall()
    return render_template('TUserRequest.html', data=data, data1=data1)


@app.route("/TApproved")
def TApproved():
    rid = request.args.get('rid')
    fid = request.args.get('fid')

    session["fid"] = fid
    session["rid"] = rid

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute("Update userfiletb set Status='ApprovedTrapdoor' where id='" + rid + "' ")
    conn.commit()
    conn.close()

    return TUserRequest()


@app.route("/serverlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'server' and request.form['password'] == 'server':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb where status='waiting'")
            data = cur.fetchall()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb where status='Active'")
            data1 = cur.fetchall()
            return render_template('ServerHome.html', data=data, data1=data1)

        else:
            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)


@app.route("/ServerHome")
def ServerHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='Active'")
    data1 = cur.fetchall()
    return render_template('ServerHome.html', data=data, data1=data1)


@app.route("/UserApproved")
def UserApproved():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='Active'")
    data1 = cur.fetchall()
    return render_template('UserApproved.html', data=data, data1=data1)


@app.route("/Approved")
def Approved():
    id = request.args.get('lid')
    email = request.args.get('email')

    import random
    loginkey = random.randint(1111, 9999)
    message = "Owner Login Key :" + str(loginkey)

    sendmsg(email, message)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute("Update ownertb set Status='Active',LoginKey='" + str(loginkey) + "' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='Active'")
    data1 = cur.fetchall()

    return render_template('ServerHome.html', data=data, data1=data1)


@app.route("/Approved1")
def Approved1():
    id = request.args.get('lid')
    email = request.args.get('email')

    import random
    loginkey = random.randint(1111, 9999)
    message = "User Login Key :" + str(loginkey)

    sendmsg(email, message)
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute("Update regtb set Status='Active',LoginKey='" + str(loginkey) + "' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='Active'")
    data1 = cur.fetchall()

    return render_template('UserApproved.html', data=data, data1=data1)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']
        gname = "A"

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "','waiting','','" + gname + "')")
        conn.commit()
        conn.close()

        alert = 'Record Saved!'
        return render_template('goback.html', data=alert)


@app.route("/newowner", methods=['GET', 'POST'])
def newowner():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ownertb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "','waiting','')")
        conn.commit()
        conn.close()

        alert = 'Record Saved!'
        return render_template('goback.html', data=alert)


@app.route("/ownerlogin", methods=['GET', 'POST'])
def ownerlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']
        loginkey = request.form['loginkey']
        session['oname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cursor = conn.cursor()
        cursor.execute("SELECT * from ownertb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)

        else:

            Status = data[7]
            lkey = data[8]

            if Status == "waiting":

                alert = 'Waiting For Server Approved!'
                return render_template('goback.html', data=alert)

            else:

                if lkey == loginkey:

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='5sharedatadbpy')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM ownertb where username='" + session['oname'] + "'")
                    data1 = cur.fetchall()
                    return render_template('OwnerHome.html', data=data1)
                else:
                    alert = 'Login Key Incorrect'
                    return render_template('goback.html', data=alert)


@app.route('/OwnerHome')
def OwnerHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where username='" + session['oname'] + "'")
    data1 = cur.fetchall()
    return render_template('OwnerHome.html', data=data1)


@app.route('/OwnerFileUpload')
def OwnerFileUpload():
    return render_template('OwnerFileUpload.html', oname=session['oname'])


def split_file(input_file, output_dir):
    # Create output directory if it doesn't exist
    filepath = input_file
    head, tail = os.path.split(filepath)
    print(head)
    # if not os.path.exists(output_dir):
    # os.makedirs(output_dir)

    # Get the size of the input file
    file_size = os.path.getsize(input_file)

    # Calculate the chunk size for each part
    chunk_size = file_size // 4

    # Open input file in binary mode
    with open(input_file, 'rb') as f:
        for i in range(4):
            # Create output file for the current part
            output_file = os.path.join(head + "/split/" + f'{i + 1}' + tail)
            print(output_file)
            with open(output_file, 'wb') as part:
                # Read a chunk of data and write it to the output file
                chunk = f.read(chunk_size)
                part.write(chunk)


@app.route("/owfileupload", methods=['GET', 'POST'])
def owfileupload():
    if request.method == 'POST':
        oname = session['oname']
        info = request.form['info']
        file = request.files['file']
        gname = "A"
        import random
        fnew = random.randint(111, 999)
        savename = str(fnew) + file.filename

        file.save("static/upload/" + savename)
        input_file = "static/upload/" + savename
        output_dir = ""

        split_file(input_file, output_dir)

        filepath = "./static/upload/" + savename
        head, tail = os.path.split(filepath)

        newfilepath1 = './static/upload/' + str(tail)
        newfilepath2 = './static/Encrypt/' + str(tail)

        newfilepath11 = './static/upload/split/1' + str(tail)
        newfilepath12 = './static/upload/split/2' + str(tail)
        newfilepath13 = './static/upload/split/3' + str(tail)
        newfilepath14 = './static/upload/split/4' + str(tail)

        enewfilepath11 = './static/Encrypt/1' + str(tail)
        enewfilepath12 = './static/Encrypt/2' + str(tail)
        enewfilepath13 = './static/Encrypt/3' + str(tail)
        enewfilepath14 = './static/Encrypt/4' + str(tail)

        secp_k = generate_key()
        privhex = secp_k.to_hex()
        pubhex = secp_k.public_key.format(True).hex()

        data = 0
        data1 = 0
        data2 = 0
        data3 = 0
        data4 = 0

        with open(newfilepath1, "rb") as File:
            data = base64.b64encode(File.read())  # convert binary to string data to read file

        with open(newfilepath11, "rb") as File:
            data1 = base64.b64encode(File.read())  # convert binary to string data to read file

        with open(newfilepath12, "rb") as File:
            data2 = base64.b64encode(File.read())

        with open(newfilepath13, "rb") as File:
            data3 = base64.b64encode(File.read())
        with open(newfilepath14, "rb") as File:
            data4 = base64.b64encode(File.read())

        if privhex == 'null':
            # flash('Please Choose Another File,file corrupted!')
            alert = 'Please Choose Another File,file corrupted!'
            return render_template('goback.html', data=alert)

        else:
            encrypted_secp = encrypt(pubhex, data)
            with open(newfilepath2, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data1)
            with open(enewfilepath11, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data2)
            with open(enewfilepath12, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data3)
            with open(enewfilepath13, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data4)
            with open(enewfilepath14, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO filetb VALUES ('','" + oname + "','" + info + "','" + savename + "','" + privhex + "','" + gname + "')")
        conn.commit()
        conn.close()

        return render_template('OwnerFileUpload.html', pkey=privhex, oname=oname)


@app.route('/OwnerFileInfo')
def OwnerFileInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb where OwnerName='" + session['oname'] + "'")
    data1 = cur.fetchall()
    return render_template('OwnerFileInfo.html', data=data1)


@app.route('/keywordInfo')
def keywordInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filekeytb where OwnerName='" + session['oname'] + "'")
    data1 = cur.fetchall()
    return render_template('OkeywordInfo.html', data=data1)


@app.route("/AddKeyword")
def AddKeyword():
    fid = request.args.get('fid')
    session['fid'] = fid
    return render_template('Newkeyword.html')


@app.route("/addnew", methods=['GET', 'POST'])
def addnew():
    if request.method == 'POST':
        kword = request.form['uname']
        fid = session['fid']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  filetb where  id='" + fid + "'")
        data = cursor.fetchone()
        if data:
            OwnerName = data[1]
            FileInfo = data[2]
            FileName = data[3]
            Pukey = data[4]
            GroupId = data[5]

        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO filekeytb VALUES ('','" + fid + "','" + OwnerName + "','" + FileInfo + "','" + FileName + "','" + Pukey + "','" + GroupId + "','" + kword + "')")
        conn.commit()
        conn.close()

        return keywordInfo()


@app.route("/ODownload")
def ODownload():
    fid = request.args.get('fid')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  filetb where  id='" + fid + "'")
    data = cursor.fetchone()
    if data:
        prkey = data[4]
        fname = data[3]

    else:
        return 'Incorrect username / password !'

    privhex = prkey

    filepath = "./static/Encrypt/" + fname
    head, tail = os.path.split(filepath)

    newfilepath1 = './static/Encrypt/' + str(tail)
    newfilepath2 = './static/Decrypt/' + str(tail)
    data = 0
    with open(newfilepath1, "rb") as File:
        data = base64.b64decode(File.read())

    print(data)
    decrypted_secp = decrypt(privhex, data)
    print("\nDecrypted:", decrypted_secp)
    with open(newfilepath2, "wb") as DFile:
        DFile.write(base64.b64decode(decrypted_secp))

    return send_file(newfilepath2, as_attachment=True)


@app.route("/OwnerFileApproved")
def OwnerFileApproved():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting' and OwnerName='" + session['oname'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='Approved' and OwnerName='" + session['oname'] + "' ")
    data1 = cur.fetchall()
    return render_template('OwnerFileApproved.html', data=data, data1=data1)


@app.route("/OApproved")
def OApproved():
    rid = request.args.get('rid')
    fid = request.args.get('fid')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  userfiletb where  id='" + rid + "'")
    data = cursor.fetchone()
    if data:
        prkey = data[4]
        UserName = data[5]
    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  regtb where  UserName='" + UserName + "'")
    data1 = cursor.fetchone()
    if data1:
        session["email"] = data1[3]
    else:
        return 'Incorrect username / password !'

    mailmsg = "Request Id" + rid + "\n Decryptkey: " + prkey

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute("update userfiletb set Status='Approved'  where id='" +
                   rid + "'")
    conn.commit()
    conn.close()

    sendmsg(session["email"], mailmsg)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting' and OwnerName='" + session['oname'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='Approved' and OwnerName='" + session['oname'] + "' ")
    data1 = cur.fetchall()
    return render_template('OwnerFileApproved.html', data=data, data1=data1)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']
        loginkey = request.form['loginkey']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)

        else:

            Status = data[7]
            lkey = data[8]
            session['gid'] = data[9]
            print(session['gid'])

            if Status == "waiting":

                alert = 'Waiting For Server Approved!'
                return render_template('goback.html', data=alert)

            else:

                if lkey == loginkey:

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='5sharedatadbpy')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
                    data1 = cur.fetchall()
                    return render_template('UserHome.html', data=data1)
                else:
                    alert = 'Login Key Incorrect'
                    return render_template('goback.html', data=alert)


@app.route('/UserHome')
def UserHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM UserHome where OwnerName='" + session['uname'] + "'")
    data1 = cur.fetchall()
    return render_template('UserHome.html', data=data1)


@app.route('/USearch')
def USearch():
    '''conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb ")
    data1 = cur.fetchall()'''
    # return render_template('USearch.html', data=data1)
    return render_template('USearch.html')


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        sear = request.form['sear']
        gid = session['gid']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM filetb where FileInfo like'%" + sear + "%'  ")
        data1 = cur.fetchall()
        return render_template('USearch.html', data=data1)


@app.route("/SendKeyRequest")
def SendKeyRequest():
    fid = request.args.get('fid')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  filetb where  id='" + fid + "'")
    data = cursor.fetchone()
    if data:

        oname = data[1]
        fname = data[3]
        prkey = data[4]
        gid = "A"
        keywww = data[2]

    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO userfiletb VALUES ('','" + fid + "','" + oname + "','" + fname + "','" + prkey + "','" + session[
            'uname'] + "','waiting','" + gid + "','" + keywww + "')")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting' and username='" + session['uname'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='Approved' and username='" + session['uname'] + "' ")
    data1 = cur.fetchall()
    return render_template('UDownload.html', data=data, data1=data1)


@app.route("/UDownload")
def UDownload():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='waiting' and username='" + session['uname'] + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
    cur = conn.cursor()
    cur.execute("SELECT * FROM userfiletb where status='Approved' and username='" + session['uname'] + "' ")
    data1 = cur.fetchall()
    return render_template('UDownload.html', data=data, data1=data1)


@app.route("/userdownload")
def userdownload():
    ufid = request.args.get('ufid')

    session["ufid"] = ufid

    return render_template('userdownload.html')


@app.route("/uddd", methods=['GET', 'POST'])
def uddd():
    if request.method == 'POST':
        sear = request.form['sear']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='5sharedatadbpy')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM  userfiletb where  id='" + session["ufid"] + "'")
        data = cursor.fetchone()
        if data:
            prkey = data[4]
            fname = data[3]


        else:
            return 'Incorrect username / password !'

        if sear == prkey:

            privhex = prkey

            filepath = "./static/Encrypt/" + fname
            head, tail = os.path.split(filepath)

            newfilepath1 = './static/Encrypt/' + str(tail)
            newfilepath2 = './static/Decrypt/' + str(tail)

            data = 0
            with open(newfilepath1, "rb") as File:
                data = base64.b64decode(File.read())

            print(data)
            decrypted_secp = decrypt(privhex, data)
            print("\nDecrypted:", decrypted_secp)
            with open(newfilepath2, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            return send_file(newfilepath2, as_attachment=True)
        else:
            return 'key Inorrect..!'


def sendmsg(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    # app.run(host='0.0.0.0',debug = True, port = 5000)
    app.run(debug=True, use_reloader=True)
