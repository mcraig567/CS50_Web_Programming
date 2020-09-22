document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#indiv-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email() {
  // Save inputs
  const email_recipients = document.querySelector('#compose-recipients').value;
  console.log("Recipients: ", email_recipients)
  const email_subject = document.querySelector('#compose-subject').value;
  console.log("Subject: ", email_subject)
  const email_body = document.querySelector('#compose-body').value;
  console.log("Body: ", email_body)

  // Create JSON and log
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: email_recipients,
      subject: email_subject,
      body: email_body
    })
  })

  .then(response => response.json())
  .then(result => {
    // print result
    console.log(result);
  });

  // Reset screen and tell user email has been sent
  load_mailbox('sent')
  alert("Email Sent")

  return false;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#indiv-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Clear any existing onclick items on archive - replace old button with new one
  let oldArchive = document.querySelector('#archive');
  let newArchive = oldArchive.cloneNode();
  let buttons = document.querySelector("#buttons");

  newArchive.setAttribute("id", "new");

  oldArchive.remove();

  // Rename new archive button for next load_mailbox call
  newArchive.setAttribute("id", "archive");
  buttons.append(newArchive);

  //Do not show the reply button if in sent folder
  if(mailbox === 'sent') {
    document.querySelector('#archive').style.display = 'none';
  } else{
    document.querySelector('#archive').style.display = 'inline';
  };

  // Clear email view div
  document.querySelector('#emails-view').innerHTML = "";

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails from API
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())

  .then(emails => {
    // Print emails
    // console.log("Getting emails...");
    emails.forEach((email) => {
          console.log(email)

      // Create element for each email
      const element = document.createElement('div');
      element.className = 'email';
      element.setAttribute("id", `email-${email["id"]}`);
      element.setAttribute("value", `${email["id"]}`);
      element.addEventListener('click', function() {
        console.log(element.id, " has been clicked");
        load_email(email);
      });

      document.querySelector('#emails-view').append(element); 
      
      console.log(element.id);

      // Create element for Sender, Title, Body and add to email element
      const sender = document.createElement('div');
      sender.innerHTML = email["sender"];
      sender.className = 'email-sender';

      const subject = document.createElement('div');
      subject.innerHTML = email["subject"];
      subject.className = 'email-subject';

      const body = document.createElement('div');
      body.innerHTML = email["body"];
      body.className = 'email-body';

      //Set background colour and font weight for read/unread emails
      if (email["read"] === true) {
        element.style.backgroundColor = 'gray';
        element.style.fontWeight = 'bold';        
      } else {
        element.style.backgroundColor = 'white';
        element.style.fontWeight = 'normal';
      }

      // Add all new elements to HTML Template 

      // Inbox gets all non-archived emails, Archive gets all others
      document.querySelector(`#email-${email["id"]}`).append(sender);
      document.querySelector(`#email-${email["id"]}`).append(subject);
      document.querySelector(`#email-${email["id"]}`).append(body);
      document.querySelector('#emails-view').append(element); 

    });

  });

}

function load_email(email) {
  console.log("loaded email: ", email)

  // Mark email as read
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });


  // Update Archive Button
  if (email["archived"] === true) {
    document.querySelector('#archive').innerHTML = 'Unarchive'
  } else {
    document.querySelector('#archive').innerHTML = 'Archive'
  };

  // Edit HTML of individual email div
  document.querySelector('#ind-email-from').innerHTML = `${email.sender}`;
  document.querySelector('#ind-email-to').innerHTML = `${email.recipients}`;
  document.querySelector('#ind-email-time').innerHTML = `${email.timestamp}`;
  document.querySelector('#ind-email-subject').innerHTML = `${email.subject}`;
  document.querySelector('#ind-email-body').innerHTML = `${email.body}`; 

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#indiv-email').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  //When clicking archive on two consecutive emails, is running archive on both emails the second time

  //Add functionality to Reply and Archive Buttons
  document.querySelector('#reply').addEventListener('click', () => reply_email(email));
  document.querySelector('#archive').addEventListener('click', () => archive_email(email));

  // Previous Event Listener which added and removed the Event Listener when the button was clicked

  // document.querySelector('#archive').addEventListener('click', function archive() {
  //  console.log("adding event listener for email ", email.id);
  //   document.querySelector('#archive').removeEventListener('click', archive);
  //  archive_email(email);
  //});
}

function reply_email(email) {
  console.log("Clicked Reply on Email: ", email.id);
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#indiv-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Autofill composition fields
  document.querySelector('#compose-recipients').value = `${email.sender}`;

  console.log("Substring: ", email.subject.substring(0,3));
  
  if (email.subject.substring(0,3) === "RE:") {
    document.querySelector('#compose-subject').value = `${email.subject}`;
  } else {
    document.querySelector('#compose-subject').value = `RE: ${email.subject}`;
  };

  document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: ${email.body}`;
}

// Archive or Unarchive based on current archive value
function archive_email(email) {

  console.log("Clicked Archive on Email: ", email.id);

  // Email is in archive
  if (email["archived"] === true) {
    console.log("Email is currently archived. Sending to inbox");
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false
      })
    })

    // Load inbox once changes complete
    .then(() => {
      console.log(`Email: ${email.id} archived should be false, is ${email.archived}`);
      load_mailbox("inbox");
    });
    

  // Email is in inbox
  } else {
    console.log("Email is not archived. Sending to archive");
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    })

    // Load inbox once changes complete
    .then(() => {
      console.log(`Email: ${email.id} archived should be true, is ${email.archived}`);
      load_mailbox("inbox");
    });
  }


}