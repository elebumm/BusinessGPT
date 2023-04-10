# BusinessGPT 📊

### Built in a couple of days as seen on my channel!

[![](https://i.imgur.com/ubCqiTm.png)](https://www.youtube.com/watch?v=nrC07M2XV1I)

#### [💬 Join the Discord! 💬](https://discord.gg/VQ5t86TEuA)

### Description 🗄️

Using GPT-4, create a business plan for your next startup! See if it's a good idea or not!

Is able to scrape websites inserted to get information about competitors and use that as information for GPT-4.

Uses SvelteKit on the frontend as a form generation!

### Disclaimer ⚠️

This is just a fun project and is not meant to be taken seriously. The code is a bit messy!

### Todos ✅

- [ ] Clean up code a little bit
- [ ] Create a better UI
- [ ] Upload to a server to allow for users to use it.
- [ ] Allow for streaming to simulate a request going much faster.

### Installation 🛠️

Make sure you have these installed:

- Docker
- A BrightData Account
  - [If you need an account you can use my referral link (Helps supports me)](https://get.brightdata.com/64n9eld4f2qd)
- An OpenAI API Key
  - If you aren't invited to GPT-4 beta, you can probably get away with the GPT-3.5 Turbo API Key

Then run the following commands:

```bash
git clone https://github.com/elebumm/BusinessGPT.git
```

```bash
cd BusinessGPT
```

```bash
docker compose up --build
```

The first time you run this, it will take a while to build the docker image. You will need to configure your BrightData proxy to spit out a file. Call this: `brightdata.json` and place it in the root of the project. This will be the settings for your proxy to connect.

### Feedback

Feel free to submit an issue or join the discord server if you want to talk about feedback or bugs!

Thanks for checking out this brief project :) Follow for more!
