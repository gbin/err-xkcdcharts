# XKCD charts in your chatroom !

This is a plugin for [Errbot](http://errbot.io) to draw XKCD looking charts in your chatroom on Slack, Hipchat...

For example:
![example](example.png?raw=true "Started using Errbot")

Be sure you have the native dependencies for Matplotlib like `freetype-dev` and `png-dev` then:
Use in a one-to-one chat `!repos install https://github.com/gbin/err-xkcdcharts` to install it.

`!help Charts` for more info.

```
Draw XKCD looking charts in your chatroom.

• ​!downchart​ - usage: downchart [-h] [--ylabel YLABEL] [--xlabel XLABEL] note
• !upchart​ - usage: upchart [-h] [--ylabel YLABEL] [--xlabel XLABEL] note
• !xy​ - usage: xy [-h] [--ylabel YLABEL] [--xlabel XLABEL] [--ylim YLIM] [--xlim XLIM]
```

Special thanks to [Randall Munroe for XKCD!](http://xkcd.com/)







