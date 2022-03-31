html_head = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Octagon Service</title>
    </head>
    <body style="padding: 35px; margin: 10px;">

    <!-- Jumbotron -->
    {body}
    <!-- Jumbotron -->


    </body>
    </html>
'''


verification_template = '''
    <div style="background-color: hsl(0, 0%, 94%); padding: 30px; border-radius: 5px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);">
        <h2 style="font-weight: 500; text-shadow: 2px 2px 5px red;">Welcome to Octagon Family!</h2>
        <p>
        Hey <b>{name}</b>, we would like to inform you that we need your photos for verification.
        </p>
        
        <p>
            <a href='{link}'>Click Here </a> for verification.
        </p>
  
       <hr style="border: 2px solid green; border-radius: 4px;">
  

        <p>Thanks<br>Team Octagon</p>
    </div>
'''


greeting_template = '''

    <div style="background-color: hsl(0, 0%, 94%); padding: 30px; border-radius: 5px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);">
        <h2 style="font-weight: 500; text-shadow: 2px 2px 5px red;">Hey {name}!</h2>
        <p>
        You've completed the verification process. Now you're part of the Octagon family. Your credentials for login:
        </p>
        
        <p>
            Username: <b>{username}</b> <br>
            Password: <b>Face Recognition</b> <br>
            <a href='{link}'>Click Here </a> to Login.
            <br>
        </p>

        <p>
        Note: Your username is the first three letters of your name + the last three digits of your number + Your Secret code. We recommend you change your secret code regularly.
        </p>
  
       <hr style="border: 2px solid green; border-radius: 4px;">
  

        <p>Thanks<br>Team Octagon</p>
    </div>

'''


message_template = '''

    <div style="background-color: hsl(0, 0%, 94%); padding: 30px; border-radius: 5px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);">
        <h2 style="font-weight: 500; text-shadow: 2px 2px 5px red;">Hey Octagon User!</h2>
        <h4 style="font-weight: 500; text-shadow: 2px 2px 5px red;">{subject}</h4>
        <p>{title}</p>
        <p>
        {message_content}
        </p>

       <hr style="border: 2px solid green; border-radius: 4px;">
  

        <p>Thanks<br>Team Octagon</p>
    </div>

'''