#
# Cookbook:: first_cookbook
# Recipe:: default
#
# Copyright:: 2020, The Authors, All Rights Reserved.
#
file "#{ENV['HOME']}/test.txt" do
  content 'This file was created by Chef Infra!'
end

execute "update-package-cache" do
    command "sudo apt-get update"
    action :run
end
