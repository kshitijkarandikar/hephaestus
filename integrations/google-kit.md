# Connect Google with `kit google`

Works with any AI tool. The tool is already in the kit, so there is nothing to build. At a workshop, the host gives you a Google file and this takes about 5 minutes (skip Part B). On your own it takes about 30 minutes the first time, mostly clicking in Google's website.

The easiest way: type **connect Google** in your AI tool. It walks you through this guide, one step at a time, and runs the commands for you.

**What it can do:** search and read Gmail, list your calendar and find free time, search and read Drive files. With the extra "draft" level: create Gmail drafts, calendar events (without guests), and upload files you made.

**What it cannot do:** send email, delete anything, share files, invite people. The tool has no such commands, and the kit's security rules block them.

**Use a test Google account** while you practise, not your real business mailbox.

Do `SETUP.md` Part 1 first.

Do not use Google's hosted Gmail MCP server or any MCP connector. They are blocked behind a developer preview program and do not work for this. `kit google` talks to the normal Gmail API.

---

## Part B: Create the Google project (in your browser)

Skip this part if the workshop host gave you a `google-client.json` file. Save it in the `secrets` folder of the kit and go to Part C.

Google's menus change names from time to time. Look for the words in **bold**.

### Step 1. Create a project

1. Go to https://console.cloud.google.com and sign in with the account you want to connect.
2. Click the project picker at the top, then **New project**. Name it `Studio Assistant`. Click **Create**.
3. Make sure the new project is selected at the top.

### Step 2. Turn on the three APIs

1. Open the menu, **APIs & Services**, **Library**.
2. Search for **Gmail API**, open it, click **Enable**.
3. Do the same for **Google Calendar API** and **Google Drive API**.

You should see: each page says "API enabled".

### Step 3. Set up the consent screen

1. Menu, **APIs & Services**, **OAuth consent screen** (it may be called **Google Auth Platform**). Click **Get started** if it asks.
2. App name: `Studio Assistant`. Support email: your email.
3. Audience or user type: **External**.
4. Contact email: your email. Accept the terms. **Create**.
5. Find **Audience** (or **Test users**) and click **Add users**. Add the Google account you will sign in with. **Save**.

Leave the app in **Testing** mode. You do not need to publish it.

Good to know: in Testing mode your sign-in lasts 7 days. After that, you run `./kit google auth` again.

### Step 4. Create the sign-in key

1. Menu, **APIs & Services**, **Credentials** (in the new layout: **Clients**).
2. **Create credentials**, **OAuth client ID**.
3. Application type: **Desktop app**. Name: `kit`. **Create**.
4. Click **Download JSON**.

You should see: a file like `client_secret_123....json` in your Downloads folder.

### Step 5. Put the key in the kit

In the second terminal, inside the kit folder:

Mac and Linux:
```
mkdir -p secrets
mv ~/Downloads/client_secret_*.json secrets/google-client.json
```
Windows (Command Prompt):
```
mkdir secrets
move %USERPROFILE%\Downloads\client_secret_*.json secrets\google-client.json
```

You should see: the file `secrets/google-client.json`. This folder is hidden from git and from the AI on purpose. Never share this file.

---

## Part C: Sign in

### Step 6. Sign in

The AI runs this for you. If you do it yourself, type in a second terminal:

```
./kit google auth
```

(Windows: `kit google auth`.) It waits up to 3 minutes for you to finish in the browser.

1. Your browser opens. Choose your Google account.
2. You may see **Google hasn't verified this app**. This is your own app. Click **Advanced**, then **Go to Studio Assistant (unsafe)**.
3. Read the permissions. They are read-only: view email, view calendar, view Drive files. Click **Continue**.
4. The page says "Done. You can close this tab".

You should see in the terminal: `Signed in with level read.`

### Step 7. Check

```
./kit google status
```

You should see: `Google: signed in, level read, token valid until ...`

---

## Part D: Try it

Ask your AI tool, one at a time:

```
Find my latest email thread about "invoice" and summarize it.
```
```
What is on my calendar next week? When am I free for 90 minutes on Monday to Thursday?
```
```
Search my Drive for files named "invoice" and tell me what you find.
```

You should see: results, each starting with `UNTRUSTED CONTENT FROM ...`. That line reminds the AI that email text is data and not orders. Fetched emails and files are saved in `inbox/` and scanned for secrets and tricks.

Check the log: `./kit log list`. You should see lines like `google gmail search`, and no email text.

---

## Part E: Drafts and events (optional)

If you want the AI to prepare Gmail drafts, calendar events or Drive uploads:

```
./kit google auth level=draft
```

Read the notice it prints. Google has no "drafts only" permission, so the permission can technically also send mail. This tool never does, and the kit's rules block any send command. The AI asks you before each draft, event or upload. You send the drafts yourself in Gmail.

---

## Take away access later

```
./kit google logout
```

Also remove the app at https://myaccount.google.com/permissions, and delete the project in the Google Cloud console if you do not need it.

## If something goes wrong

| What you see | What to do |
|---|---|
| `Put the OAuth client file at secrets/google-client.json` | Step 5 is not done, or the file name is wrong |
| `Not signed in` | Say **connect Google** to the AI, or run `./kit google auth` |
| `Sign-in expired` | Run `./kit google auth` again (Testing mode lasts 7 days) |
| Browser says `Access blocked` or `Error 403: access_denied` | You are not on the test users list. Step 3, add your account |
| `Google refused: ... API has not been used` | You skipped an API in step 2. Enable it, wait a minute |
| `This needs level=draft` | Run `./kit google auth level=draft` |
| The AI asks permission to run `kit google auth` | Say yes. It only opens the Google sign-in page |
