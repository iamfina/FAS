#!/bin/sh

IFS="
"

for line in `cat userlist`; do
  test -z "$line" && continue
  user=`echo $line | cut -f 1 -d' '`
  echo "adding user $user"
  useradd -m -s /bin/bash $user
  cp /var/tmp/MANUAL.ipynb /home/$user/MANUAL.ipynb
  chown -R $user:$user /home/$user
done

jupyterhub