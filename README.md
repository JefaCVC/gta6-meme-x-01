# WASTED: 13 years waiting for GTA 6

Entry for the make.fun bounty "Post a GTA 6 meme on X" (`gta6-meme-x-01`).
Top 50 share $500; an AI judge compares posts two at a time. Likes, reposts,
replies and views never count.

## The meme

GTA's iconic WASTED screen, but the thing wasted is 13 years of waiting for
GTA 6. Vice City sunset over Leonida: synthwave sun, skyline, palms, five
wanted stars. The make.fun ghost badge sits in the bottom band next to the
pitch, in the meme's own voice: "my AI agent earned real money while I
waited / make.fun".

The picture is `meme.png` (1200x675), drawn in code by `build_meme.py`
(Pillow, standard library plus Pillow for the build step only). The ghost
mark is make.fun's own press-kit `mark-1024.png`. Rebuild it with:

    python3 build_meme.py

Every label was checked at 30% scale and stays legible.

## The post

Post `meme.png` as the first picture from a public X account with this text
(`POSTING.md` has the exact copy):

> GTA 6 is finally here after 13 years, and I have booked a very suspicious
> sick day.
>
> While I waited, my AI agent earned real money on make.fun. Yours can too.
>
> https://make.fun/bounty/gta6-meme-x-01
> makefun-chess-coast-granary

Then put the post's address in `POST.json`:

    {"url": "https://x.com/<handle>/status/<id>"}

`POST.json` still holds the starter placeholder until the post exists. The
gate refuses the placeholder on purpose, so do not submit before the post
is live and `POST.json` names it.

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` to the
output directory. That is all it has to do; the house reads the post
itself from X. Run it the way the grader does:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`.

## Before you submit

From the kit's directory, run the pre-submit checks with the transcripts
of the sessions that made the meme and wrote this repository:

    node cli/makefun.mjs check --kit . --repo <this repository> --transcripts transcripts.tar.gz

Then submit as the kit's `RULES.txt` gives it. Keep the post up and the
account public until the results are out.
