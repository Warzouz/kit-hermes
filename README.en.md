# Hermes starter kit

[Guide français](README.md)

Status: complete local kit, version 0.1.0. `SOUL.md` includes the first-run
questionnaire instructions. This version is not published yet.
See [actual test results](docs/TESTS.md).

This kit prepares one coordinator, four subagent routes, and a review method.
It includes no AI subscription, API credit, or connected account. Desktop
onboarding and automatic questionnaire startup in a real AI conversation
remain untested.

## 1. Install Hermes

Install Hermes Desktop using the [official guide](https://hermes-agent.nousresearch.com/docs/user-guide/desktop)
for Windows, macOS, or Linux. Hermes 0.22.5 is required; later versions have not
been tested. Connect a provider in model settings before starting a conversation.
A consumer chat subscription does not necessarily grant API access.
Read [provider caveats](skills/premier-demarrage/references/acces.md).
Enter keys and login codes only in Hermes login screens, never in chat.

## 2. Install the local kit

The kit is available at `https://github.com/Warzouz/kit-hermes`.
Download it (green “Code” button, then “Download ZIP”) and unzip it.
Then open a terminal **in that folder**,
containing `distribution.yaml`:

- Windows: right-click the folder and choose “Open in Terminal”.
- macOS: open Terminal, type `cd `, drag the folder in, then press Enter.
- Linux: use the file manager's “Open in Terminal” action.

The same command works on all three systems when the Hermes CLI is on PATH:

```text
hermes profile install . --name kit-hermes
```

Read the preview and confirm. If `hermes` is not found, Desktop may not expose
its CLI on PATH. Follow the platform-specific
[installation guide](https://hermes-agent.nousresearch.com/docs/getting-started/installation);
do not blindly install a second runtime. If the profile already exists, stop and
follow the update procedure rather than `--force`. No `--alias` is required.

## 3. Select and connect the profile

Choose `kit-hermes` in Desktop's profile list. If missing, check that Desktop and
the terminal use the same Hermes storage location, then restart Desktop. There is
one profile, not four independent profiles. Connect a model in this profile's
settings, or use:

```text
hermes -p kit-hermes model
```

Do not assume another profile's login is available. The coordinator must never
copy credential stores between profiles.

## 4. Answer the questions

In a new conversation, say “Set up my coordinator”. The coordinator should ask
language, tone, AI access, budget, uses, autonomy, and channel, one at a time.
When no preferences have been saved yet, the SOUL instructions ask the coordinator
to load `premier-demarrage`. This startup still needs a real AI conversation test.

With your consent it installs the official `advanced-delegation` plugin, backs up
affected settings, and prepares `rapide`, `standard`, `profond`, and `code` routes.
Usage selections install no third-party packs. Available tools depend on your
Hermes installation. One model can serve all routes; distinct reasoning efforts
require model support. Economical mode does not guarantee a monetary ceiling.

Open a new conversation when asked, then say “Finish setup”. Real route tests
consume provider quota or credits and require consent first. Cross-model review
remains unperformed if no second model is accessible. Telegram is only a saved
preference until separately connected in messaging settings. Never paste its
secrets into the conversation.

## 5. Change choices and update

Say “Run setup again”. Preferences live in `local/kit/preferences.json` inside
the profile and survive kit updates. Before updating, close profile conversations,
find its folder through `hermes profile info kit-hermes`, and make a private backup
using your file manager. That backup may contain secrets: never share it or store
it in the kit repository.

Keep the original source folder in place, replace its kit files with the newly
received version, then run:

```text
hermes profile update kit-hermes
```

Read the preview and confirm. Config is preserved by default, while shipped skills
and SOUL are replaced. Do not customize those files. Avoid `--force-config`, which
resets configuration, and do not use a forced reinstall as an update.

## Evidence and limitations

See [decisions](DECISIONS.md), [source verification](docs/VERIFICATIONS.md),
[executed tests](docs/TESTS.md), and [scope](CAHIER-DES-CHARGES.md).
Linux technical tests do not establish Windows/macOS or real AI onboarding success.
This kit does not sandbox your computer. Read approval prompts before accepting.
MIT license: [LICENSE](LICENSE).
