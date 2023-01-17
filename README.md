You need to configure your router to declare this as the local DNS server,
similar to how you would if you were setting up a PiHole. If PiHole is in use,
first use the `stop_pihole` script to stop it, then run the script (running
the `start_pihole` script once you're done).

This is very limited in what it can do, since HSTS is now standard for most
major websites. The only way to bypass this is to remove the HSTS entry in the
user's browser, or get them to type `thisisunsafe`.

Please don't use this for malicious purposes; it was written to be an April
Fool's joke.
