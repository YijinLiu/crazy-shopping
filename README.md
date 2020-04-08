# A simple online shopping automation tool
==========================================

At this special moment, many of us are buying food online. If you have experienced difficulty in
checking out your shopping carts because of stock / delivery issues, you may end up keeping
refreshing some web pages manually all the time. This is time consuming and exhausting.
This project presents a simple tool to automate it. You drop items in the shopping carts and
leave the checkout to the machine.

## Table of contents
  * [Manual](#manual)
    * [Wholefood](#wholefood)
  * [For developer](#for-developer)


## Manual
Create the docker container:
<pre>
$ docker run -it --shm-size 2g --name crazy-shopping yijinliu/crazy-shopping:2020-04-08
</pre>

Inside the container:
<pre>
$ git clone https://github.com/YijinLiu/crazy-shopping
$ cd crazy-shopping
</pre>

### Wholefood
Add products to your cart and run following command in the container:
<pre>
$ ./wholefood.py --email "xxxx@yyyy" --password "zzzz"
</pre>

## For Developer.
To build a new docker image:
<pre>
$ make
</pre>
To be able to run in non headless mode:
<pre>
$ docker run -it -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/snd --shm-size 2g --name crazy-shopping yijinliu/crazy-shopping:2020-04-08
</pre>
