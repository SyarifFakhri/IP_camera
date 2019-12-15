These commands have to run as sudo, so you have to allow them in the linux file path.
1.
Run: 
> sudo visudo -f /etc/sudoers

I'm not sure what's the difference between doing this and "sudo visudo", but both seem to work
2. 
At the end add the line
haq ALL=(root) NOPASSWD: /home/haq/repos/IP_camera/src/sh_scripts/deauthorize_device.sh
haq ALL=(root) NOPASSWD: /home/haq/repos/IP_camera/src/sh_scripts/reauthorize_device.sh

3. 
Voila you can now run sudo in python without having to put a password

p.s. Don't forget to make them executable when you copy them over

