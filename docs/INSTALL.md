# Install Build with Amplifier

## Portable method

Requires Git and Python 3.11+. From a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-build-amplifier.git
cd amplifier-skill-build-amplifier
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The destination is the parent of the `build-amplifier` folder. Select your host’s supported skills location. Refresh skill discovery, or point your agent at the complete installed folder and ask it to read `SKILL.md`.

Try this first:

```text
Use Build with Amplifier to inspect this repository. I want a progress panel for a long-running tool. Decide where the feature belongs, identify the actual event contract, and propose one slice with cancellation and cleanup checks.
```

## Install behavior and optional execution

Run `python3 scripts/capability.py doctor`, then `python3 scripts/capability.py install --dest <your-host-skills-parent>`. The destination must be the parent of the installed `build-amplifier` folder. The command refuses conflicting content; inspect it before choosing `--replace`, which retains a dated backup. Repeating an identical install is idempotent. Remove only that installed folder to uninstall; no global service is installed.

The portable method requires no engine, provider credential, Memory service, or background process. Native runtime instructions are retained in [the native guide](NATIVE-README.md), with their original dependencies and limitations. Check the actual host/version/permissions before execution. A method doctor result is not runtime health or model quality evidence.