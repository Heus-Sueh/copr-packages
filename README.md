# COPR Repository

This COPR repository provides packages for applications that are not yet available in the official Fedora repositories, allowing Fedora users to easily install and try out new software.

## About

The purpose of this repository is to give Fedora users access to applications that haven’t been added to the official repositories, either because they’re new, alternative options, or still in the process of becoming officially integrated.

## Usage

### Enabling the COPR Repository on Fedora

1. First, enable the COPR repository with the following command:

   ```bash
   sudo dnf copr enable heus-sueh/packages
   ```

2. Then, install the desired application:

   ```bash
   sudo dnf install [application-name]
   ```

   > **Note:** Replace `[application-name]` with the specific name of the application you wish to install.

### Enabling the COPR Repository on Fedora Silverblue (Atomic)

Fedora Silverblue uses an immutable file system, so applications need to be installed using `rpm-ostree`. You can simplify COPR repository management with the [COPR-command](https://github.com/boredsquirrel/COPR-command) script, which makes enabling and managing COPR repositories easier on Silverblue.

To set up COPR-command quickly, use the following commands:

1. Download and make the script executable:

   ```bash
   wget https://raw.githubusercontent.com/boredsquirrel/COPR-command/main/copr -P ~/.local/bin/ && \
   chmod +x ~/.local/bin/copr
   ```

2. Ensure `~/.local/bin` is in your PATH by adding the following line to your shell configuration file (`~/.bashrc` or `~/.bash_profile` for Bash, `~/.zshrc` for Zsh):

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. Reload your shell configuration to apply the PATH update:

   ```bash
   source ~/.bashrc  # or source ~/.zshrc for Zsh
   ```

Once set up, you can enable a COPR repository with:

```bash
copr enable heus-sueh/packages
```

After enabling the repository, install the desired application with `rpm-ostree`:

```bash
sudo rpm-ostree install [application-name]
```

Reboot your system to apply the changes:

```bash
systemctl reboot
```

> **Note:** COPR-command simplifies the `copr enable` step on Silverblue, making COPR repository management in an immutable environment more convenient.

## Available Applications

This repository currently includes the following applications:

- **Matugen** - A material you color generation tool
- **Clipse** - Configurable TUI clipboard manager for Unix 
- **Cliphist** - wayland clipboard manager with support for multimedia

> The list is updated as new applications are added. Check back regularly for updates!

## Feedback and Contributions

If you encounter any issues or have suggestions for new applications to include, feel free to [open an issue](https://github.com/Heus-Sueh/copr-packages/issues) or get in touch.
