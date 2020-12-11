## 1. Getting ready guide  

This is not a quick-start guide in the traditional sense. But there are always several things that are __assumed__ to be true that benefit from additional explanation.

### How to setup signed commits on your Mac

This method is based on using your personal KeyBase account. Use of Keybase is not a requirement for signed commits and there are many posts you can find that describe alternative means. Many people already use some popular keyserver (e.g., pgp.mit.edu, keyserver.ubuntu.com)

Requirements:
* Github account
* Keybase account
* GPG service locally

```bash
$ brew cask install Keybase
$ brew install gpg
```

Create new personal key. (Note: you can skip if you already maintain your key via alternative means)
```bash
$ Keybase pgp gen —multi

# If your gpg is running local then you should see the following

Enter your real name, which will be publicly visible in your new key: Jane DOe
Enter a public email address for your key: jdoe@thoughtworks.com
Enter another email address (or <enter> when done): jane.doe@gmail.com
Enter another email address (or <enter> when done):
Push an encrypted copy of your new secret key to the Keybase.io server? [Y/n] Y
When exporting to the GnuPG keychain, encrypt private keys with a passphrase? [Y/n] Y
▶ INFO PGP User ID: Jane Doe <jdoe@thoughtworks.com> [primary]
▶ INFO PGP User ID: Jane Doe <jane.doe@gmail.com>
▶ INFO Generating primary key (4096 bits)
▶ INFO Generating encryption subkey (4096 bits)
▶ INFO Generated new PGP key:
▶ INFO   user: Jane Doe <jdoe@thoughtworks.com>
▶ INFO   4096-bit RSA key, ID A8E47C364353308EC9, created 2020-05-25
▶ INFO Exported new key to the local GPG keychain
```

List info needed to setup git locally

```bash
$ gpg --list-secret-keys --keyid-format LONG                                                (Python 3.7.7)
/Users/ncheneweth/.gnupg/pubring.kbx
------------------------------------
sec   rsa4096/A8E47CAE38308EC9 2020-05-25 [SC] [expires: 2036-05-21]
      7703E0D1ECF17C64C6B09DDFA8E47CAE38308EC9
uid                 [ unknown] Jane Doe <jdoe@thoughtworks.com>
uid                 [ unknown] Jane Doe <njane.doe@gmail.com>
ssb   rsa4096/55AD50E8A4EF5CE5 2020-05-25 [E] [expires: 2036-05-21]

# add to git config

$ git config --global user.signingkey A8E47CAE38308EC9
$ git config --global commit.gpgsign true

# copy to clipboard for pasting into github
keybase pgp export -q 5BE03B7DE63C0271 | pbcopy

# test
export GPG_TTY=$(tty)
echo "test" | gpg --clearsign

# Set as default gpg key
$ $EDITOR ~/.gnupg/gpg.conf

# Add line:
default-key E870EE00
```
There are couple different common ways of getting your local config to know to use the key for signing every time. 

```bash
$ brew uninstall pinentry-mac
```

Some people find that pinentry installed with brew does not allow the password to be saved to macOS's keychain.
If you do not see "Save in Keychain" after following Method 1, try the GPG Suite versions, available from gpgtools.org, or from brew by running:

```bash
$ brew cask install gpg-suite
```

Once installed, open Spotlight and search for "GPGPreferences", or open system preferences and select "GPGPreferences." Select the Default Key if it is not already selected, and ensure "Store in OS X Keychain" is checked.

### more
