# Website Image Downloader #

Not endorsing the illegal usage of image's licenses

## :bookmark_tabs: Contents

1. [:book: Description](#-description)
1. [🧱 Tech stack](#-tech-stack)
1. [:desktop_computer: Usage](#-usage)
    1. [:nerd_face: Pre-requisites](#-pre-requisites)
    1. [🛠️ How to configure it](#-how-to-configure-it)
    1. [🐱‍💻 By command](#-by-command)
    1. [🛎️ By prompt](#-by-prompt)
1. [⚖️ Legal notice](#-legal-notice)

## :book: Description
[⬆ Back to top](#-contents)

Basic project with the idea of downloading ALL of the images from a website page (just the page).

## 🧱 Tech stack
[⬆ Back to top](#-contents)

**Python**, I've chosen python since it's the go-to for webscraping, and incredibly easy language with tons of libraries tuned and ready for almost everything you may want to do, and it's concurrency features are quite easy to grasp.

## :desktop_computer: Usage
[⬆ Back to top](#-contents)

It's not too in-detail since it's not a big project.

### :nerd_face: Pre-requisites
[⬆ To the section](#-usage)

- Having Python >= `3.6.x` installed, currently I have installed `3.8.4`.
- Having access to internet and the pages you want to modify, this step is important, if your proxy is blocking the access, this script won't bypass it.

Also, you'll need to download this package locally for it work, since it's not deployed on a website, and, for legal reasons, I do not feel safe deploying it myself.

```bash
git clone https://github.com/jofaval/page-img-downloader
cd page-img-downloader
```

### 🛠️ How to configure it
[⬆ To the section](#-usage)

1. Head to the `config.py` file, which holds the configuration for the package.
1. Some websites may require an specific header, you can change the `HEADERS` to your preference
1. You may not want to use all your processors, if that were to be the case, override the `THREADS_LIMIT` variable.
1. I'd recomend to leave it with `DEBUG` mode on, but you may not care about it, you'll only lose feedback and insights, nothing else.
1. If you want to change the locale of the package, change the `DEFAULT_LOCALE` to your preference, you could even create your own locale!
1. You can also modify the messages by updating the `STRINGS` constants.
1. `IMAGES_DIR` will indicate where the package will store the images, by default, at this directory.
1. And, finally, only if `DEBUG` mode is enabled, you can change the logging configuration, if left as is, it will log information to the `log.txt` file at the root of this package's directory.

### 🐱‍💻 By command
[⬆ To the section](#-usage)

Remmeber that it's important to be at the package's root directory.

```bash
cd page-img-downloader
```

If you're using a Linux system, you'll have to call the `python3` command.

```bash
python3 script.py https://my.website.com/path/to/page/
```

Or in my case, if you're on Windows, this will be the script that will work

```bash
python script.py https://my.website.com/path/to/page/
```

### 🛎️ By prompt
[⬆ To the section](#-usage)

You could let the package ask you for the website.

```bash
python3 script.py
```

Which will prompt: _What website would you want to download from?_
And you can paste the website that you want: https://my.website.com/path/to/page/

## ⚖️ Legal notice
[⬆ Back to top](#-contents)

As aforementioned, I do not endorse it's illegal use, each image holds accountable to some license, and it's rightfully owner(s). Use it with caution and on websites that do allow for this kind of explotation (also checkout the _robots.txt_ of the page).