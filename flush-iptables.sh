#!/bin/bash

# Flush all the rules from iptables
iptables -F
ip6tables -F

# Delete all the custom chains
iptables -X
ip6tables -X

# Set default policies to allow all traffic
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
ip6tables -P INPUT ACCEPT
ip6tables -P OUTPUT ACCEPT
ip6tables -P FORWARD ACCEPT

# Accept all incoming connections and all ports
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 1:65535 -j ACCEPT
iptables -A INPUT -p udp -m udp --dport 1:65535 -j ACCEPT
ip6tables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
ip6tables -A INPUT -p tcp -m tcp --dport 1:65535 -j ACCEPT
ip6tables -A INPUT -p udp -m udp --dport 1:65535 -j ACCEPT

# Display the new rules
iptables -L -v -n
ip6tables -L -v -n

# Save the changes to iptables
iptables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6
