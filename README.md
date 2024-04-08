# STAR Assessments course repo

Please check out the [csxxx wiki](https://github.com/ace-lab/pl-ucb-csxxx/wiki)
for basic PrairieLearn mechanics etc.

Here's where to put your stuff.  In the examples below, substitute a
name/moniker for your course in place of `PROJECT`.

**Remember:** it's fine to copy boilerplate files from other
directories, but **every PL item has a unique UID (uuid)** and you
have to change those.  You can generate UUIDs with the shell command `uuidgen`.

## Develop on a branch

To avoid lots of merge collisions, it's best to do all of the below on a branch
and use that branch for local testing.  When ready, open a pull request to merge
your branch to `master` and we will do the merge.  Note that the PR
should **only** result in changes to `questions/PROJECT/`, `courseInstances/PROJECT/`, and possibly
adding a new directory under `elements/`.  PRs that make other changes besides
those will be rejected unless accompanied by an explanation.

## Create and git add the directory `courseInstances/PROJECT`

In it you'll need a minimal `infoCourseInstance.json`, which you can
base on an existing one, but don't forget to change the uuid's.

## Create and add `questions/PROJECT/`

This is where your example question(s) will go.

## If you're building an element, create and add `elements/pl-*`....

...where * is whatever your element name is.

**At this point**, all of your work should be able to go into either a
question subdirectory or the element subdirectory.  If you find
yourself in a situation where you have code that doesn't belong in
either of those places, ask us.  The reason is to keep each project
standalone: it should be possible for an instructor to use the project
simply by copying any `questions/CS999/` subdirectories and optionally
any element subdirectories, nothing else.


## Packaging milestone

You've achieved the packaging milestone when you can render one
question (even if grading doesn't fully work yet) that has its files
placed as described above.
