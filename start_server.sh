f ! screen -list | grep -q "minecraft"; then
  export PATH=$PWD/jdk-16.0.1+4/bin:$PATH
  cd /home/cowman/minecraft
  screen -S minecraft -d -m java -jar -Xms512M -Xmx3G spigot-1.17.1.jar nogui 
fi