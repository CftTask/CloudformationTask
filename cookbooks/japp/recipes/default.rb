execute "update" do
    command "sudo yum update -y"
    action :run
end


# setup nginx
execute "add epel repo" do
    command "yum install -y epel-release"
    action :run
end

execute "install nginx" do
    command "sudo yum install -y nginx"
    action :run
end

execute "add runlevel to nginx" do
    command "sudo chkconfig nginx on"
    action :run
end

cookbook_file '/etc/nginx/nginx.conf' do
  source 'nginx.conf'
  owner 'root'
  group 'root'
  mode '0644'
  action :create
end


# setup docker djapp
execute "install docker" do
    command "sudo yum install -y docker"
    action :run
end

execute "add runlevel to docker" do
    command "sudo chkconfig docker on"
    action :run
end

execute "start docker" do
    command "sudo service docker start"
    action :run
end

execute "add user to docker" do
    command "sudo usermod -a -G docker ec2-user"
    action :run
end

execute "pull docker image" do
    command "docker pull karrug/djapp:0.4"
    action :run
end

cookbook_file '/etc/init.d/djapp' do
  source 'services/djapp'
  owner 'root'
  group 'root'
  mode '0755'
  action :create
end

execute "add djapp service" do
    command "sudo chkconfig --add djapp"
    action :run
end

execute "add runlevel to djapp" do
    command "sudo chkconfig djapp on"
    action :run
end
