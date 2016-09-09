The Mindbites video downloader can be used to download a portion or all of the videos which are present within a [Mindbites](http://mindbites.com) course. This tool enables you to easily download the desired number of videos in bulk from a course without manually obtaining them from the website and renaming them on your own, one by one.

# Getting Started

Please install [Python 3](https://www.python.org/downloads/) on your computer. After the installation has completed, install the necessary Python libraries:

```sh
$ sudo pip install lxml==3.6.0
$ sudo pip install requests
```

# Configuration

This tool contains a `replace.ini` file. By default, the program will try to provide a good name to all of the files which it is downloading. However, in cases where you do not like the way a video has been named, you may provide a list of phrases to replace, as below:

```
[mindbites]
"Olivers": "Oliver's"
"Of The Time": "of the Time"
"Int ": "Intermediate "
```

Things to note:
- Do not put commas at the end of each line, just follow the `"words to find": "words to replace"` convention.
- Do not remove the `[mindbites]` line at the beginning of the file. This must be at the top.

# Examples

When running this tool, you need, at a minimum, the following pieces of information:

- **Course name:** `-c` or `--course`
- **Mindbites account email address:** `-e` or `--email`
- **Mindbites account password:** `-p` or `--password`
- **Course URL:** `-u` or `--url`

#### Minimalist Example

Downloads all of the videos from a Calculus course to the local folder.

```sh
python mindbites.py --course "Calculus" --email "email@example.com" --password "mypassword!" --url "www.mindbites.com/series/227-calculus"
```

#### Preview before Downloading

Shows all of the videos which will be downloaded, along with the names they will be given. This is helpful if you want to check if the names are to your liking or if you will be downloading all of the videos you want before actually starting the process.

```sh
python mindbites.py --course "Calculus" --email "email@example.com" --password "mypassword!" --url "www.mindbites.com/series/227-calculus" --view true
```

#### Download a Range of Videos:

Downloads video numbers 7 through 42, inclusive, from a Calculus course to the local folder.

```sh
python mindbites.py --course "Calculus" --email "email@example.com" --password "mypassword!" --url "www.mindbites.com/series/227-calculus" --start 7 --finish 42
```

# Explaination of all Switches

In addition to the required switches mentioned above, there are a few optional ones which are explained here.

#### Required

When running this tool, you need, at a minimum, the following pieces of information:

Name | Short Switch | Descriptive Switch | Explaination | Default Value
--- | --- | --- | --- | ---
Course Name | `-c` | `--course` | The name of the course from which you will be downloading | <None>
Email Address | `-e` | `--email` | Your Mindbites login email | <None>
Password | `-p` | `--password` | Your Mindbites login password | <None>
Course URL | `-u` | `--url` | The link to the course from which you will be downloading videos | <None>

#### Optional

For enhanced functionality, you may also use the following switches:

Name | Short Switch | Descriptive Switch | Explaination | Default Value
--- | --- | --- | --- | ---
Finish | `-f` | `--finish` | Download up to and including this video number from the list of videos in the course | `9999`
Out | `-o` | `--out` | The folder where all of the downloaded videos should appear | `./` (Current folder)
Replace File | `-r` | `--replace` | The path to the `replace.ini` file | `./replace.ini`
Start | `-s` | `--start` | Download starting from and including this video number from the list of videos in the course | `1`
Preview | `-v` | `--view` | Preview the list of videos and their names without actually downloading them. Use `true` as the parameter if you want to preview the video list. | `false`