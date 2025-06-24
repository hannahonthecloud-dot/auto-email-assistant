# Auto Email Assistant: Send Emails from Google Sheets (AltSchool Project)

Hey there! 👋

This project is called **Auto Email Assistant** and I built it as part of my submission for the PipeOps challenge on AltSchool. It lets you send personalized emails to recruiters straight from a Google Sheet using a Python script. Once the email is sent, it marks that row so it doesn’t send it again.

If you’ve ever wanted a way to manage follow-up or thank-you emails after job applications automatically, this is for you.

Let me walk you through exactly how to get it working, from setting up your Google Cloud project to running the script and watching your emails go out.

---

## 🛠 What You’ll Need

- A Google Account
- Python installed on your system
- A virtual environment (optional but clean!)
- Access to Google Cloud Console
- A Google Sheet that tracks your job applications

---

## 🚀 Step 1: Set Up Your Google Cloud Project

This part is necessary to get access to the Gmail and Google Sheets APIs.

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)

2. Click "Create Project" and give it a name like `auto-email-assistant`

3. After creating it, go to the sidebar, search for **"APIs & Services" > Library**

4. Enable these APIs:

   - Gmail API
   - Google Sheets API
   - Google Drive API

5. Now go to **"Credentials"** and click **"Create Credentials" > OAuth client ID**

6. Choose **Desktop App**

7. Download the file called `client_secret_XXX.json` and save it in your project folder

---

## 🧪 Step 2: Set Up Your Python Environment

1. In your terminal, navigate to your project folder:

```bash
cd ~/G-mail-script
```

2. Create and activate a virtual environment:

```bash
python3 -m venv myemailprojectenv
source myemailprojectenv/bin/activate
```

3. Install required libraries:

```bash
pip install --upgrade pip
pip install --upgrade google-api-python-client google-auth google-auth-oauthlib gspread oauth2client
```

---

## 🧾 Step 3: Prepare Your Google Sheet

Open a new Google Sheet and call it something like **"JOB TRACKING"**. Here’s how the table should look:

| Company | Role           | Recruiter Name | Recruiter Email                              | Email Type | Sent |
| ------- | -------------- | -------------- | -------------------------------------------- | ---------- | ---- |
| Google  | Cloud Engineer | Linda A.       | [linda@google.com](mailto\:linda@google.com) | thank-you  | No   |

- Make sure these are the **exact headers** in your header row. 
- "Email Type" should be either `thank-you` or `follow-up`
- "Sent" should start with `No` so it knows what to send.

---

## 💌 Step 4: Create Your Email Templates

Inside your project folder, make a folder called `templates`. Create two files:

### `Thank-you.txt`

```
Subject: Thank you for the {{role}} interview at {{company}}

Hi {{recruiter_name}},

Thank you for speaking with me about the {{role}} role at {{company}}. It was a pleasure chatting with you.

Wishing you a great week,
Ngozi Hannah Opara
```

### `Follow-up.txt`

```
Subject: Following up on the {{role}} position at {{company}}

Hi {{recruiter_name}},

I wanted to follow up on my application for the {{role}} role at {{company}}. I'm still very interested and would love to hear your feedback.

Kind regards,
Ngozi Hannah Opara
```

---

## 🧠 Step 5: How the Python Script Works (in plain language)

Let’s break this into blocks.

### 🔐 1. Authenticate Gmail

This part logs you into Gmail using your credentials and lets the script send emails for you.

### 📄 2. Connect to Google Sheets

Here, we open your sheet, find the row where the actual table starts (we used `head=4`), and read all the rows.

We clean up the data so it’s easier to access (for example, we treat column names like `company`, `role`, etc. in lowercase).

### 📧 3. Create Email Message

We build the email body by loading the correct template and replacing:

- `{{company}}` with the actual company name
- `{{role}}` with the job title
- `{{recruiter_name}}` with the recruiter’s name

### ✅ 4. Send Emails

For each row where the "Sent" column is `No`, we:

- Load the correct template
- Customize the message
- Send it using Gmail
- Update the "Sent" column to `Yes`

We also print a message in the terminal so you can see what’s happening live.

---

## 🔗 Step 6: Connect to GitHub and PipeOps (Optional for Automation)

If you want to go further and automate this with PipeOps:

1. Push this project to a GitHub repo
2. Log into your PipeOps account
3. Connect your GitHub account to PipeOps
4. Create a new **Pipe** that runs your script on a schedule or when you click "Run"
5. Use a build step like:

```bash
python send-emails.py
```

Now, even if you’re not on your laptop, you can still send your emails in one click from the cloud. 🌥

---

## 🙌 Wrap-up

That’s it! You now have a system that reads your job tracker, sends personalized thank-you or follow-up emails, and updates the sheet so you don’t send duplicates.

If you want to improve it later, here are a few ideas:

- Add file attachment support (like CVs)
- Schedule emails
- Integrate it into a web dashboard

Hope this helped!

If you run into issues or want to see a demo, feel free to reach out.

With grit and Gmail, Ngozi Hannah Opara ✨

