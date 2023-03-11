
import random
import numpy as np
from tqdm import tqdm
import torch
from torch import nn
import torch.nn.functional as F
import rl_utils


# class PolicyNetContinuous(torch.nn.Module):
#     def __init__(self, state_dim, hidden_dim, hidden_dim2, action_dim,action_dis_dim):
#         super(PolicyNetContinuous, self).__init__()

#         self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
#         self.fc2 = torch.nn.Linear(hidden_dim, hidden_dim2)

#         self.fc_mu = torch.nn.Linear(hidden_dim2, action_dim)
#         self.fc_std = torch.nn.Linear(hidden_dim2, action_dim)

#         self.fc_a_dis = torch.nn.Linear(hidden_dim2, action_dis_dim)



#     def forward(self, x):
#         x = F.relu(self.fc1(x))

#         x = F.relu(self.fc2(x))

#         mu = torch.tanh(self.fc_mu(x))
#         std = F.softplus(self.fc_std(x))

#         a_dis = F.softmax(self.fc_a_dis(x), dim=1)


#         return mu, std, a_dis
    

# class ValueNet(torch.nn.Module):
#     def __init__(self, state_dim, hidden_dim, hidden_dim2):
#         super(ValueNet, self).__init__()
#         self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
#         self.fc2 = torch.nn.Linear(hidden_dim, hidden_dim2)

#         self.fc3 = torch.nn.Linear(hidden_dim2, 1)

#     def forward(self, x):
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         return self.fc3(x)    

# class PPOContinuous:
#     ''' 处理连续动作的PPO算法 '''
#     def __init__(self, state_dim, hidden_dim, hidden_dim2, action_dim,action_dis_dim, actor_lr, critic_lr,
#                  lmbda, epochs, eps, gamma, device):
#         # 定义 actor
#         self.actor = PolicyNetContinuous(state_dim, hidden_dim,hidden_dim2,
#                                          action_dim,action_dis_dim).to(device)
        
#         # 定义 critic
#         self.critic = ValueNet(state_dim, hidden_dim,hidden_dim2).to(device)

#         # 
#         self.actor_optimizer = torch.optim.Adam(self.actor.parameters(),
#                                                 lr=actor_lr)
        

#         self.critic_optimizer = torch.optim.Adam(self.critic.parameters(),
#                                                  lr=critic_lr)
        
#         # discount
#         self.gamma = gamma

#         self.lmbda = lmbda

#         self.epochs = epochs
#         self.eps = eps

#         self.device = device

#     def take_action(self, state):
        
#         state = torch.tensor([state], dtype=torch.float).to(self.device)
#         mu, sigma, probs = self.actor(state)

#         action_dist = torch.distributions.Normal(mu, sigma)

#         action = action_dist.sample()

#         action_dis_dist = torch.distributions.Categorical(probs)
#         action_dis = action_dis_dist.sample()

        
#         l_action = action.cpu().tolist() 
        

#         return l_action[0], action_dis.item()

#     def update(self, transition_dict):
#         states = torch.tensor(transition_dict['states'],
#                               dtype=torch.float).to(self.device)
        
#         actions = torch.tensor(transition_dict['actions'],
#                                dtype=torch.float).to(self.device)
        
#         # actions = torch.tensor(transition_dict['actions'],
#                             #    dtype=torch.float).view(-1, 1).to(self.device)
        
        
        

        
#         actions_dis = torch.tensor(transition_dict['actions_dis']).view(-1, 1).to(
#             self.device)
        
#         # print(actions)
#         # print(actions_dis)

#         rewards = torch.tensor(transition_dict['rewards'],
#                                dtype=torch.float).view(-1, 1).to(self.device)
        
#         next_states = torch.tensor(transition_dict['next_states'],
#                                    dtype=torch.float).to(self.device)
#         dones = torch.tensor(transition_dict['dones'],
#                              dtype=torch.float).view(-1, 1).to(self.device)
        

#         rewards = (rewards + 20.0) / 20.0  # 和TRPO一样,对奖励进行修改,方便训练


#         td_target = rewards + self.gamma * self.critic(next_states) * (1 -
#                                                                        dones)
#         td_delta = td_target - self.critic(states)
#         advantage = rl_utils.compute_advantage(self.gamma, self.lmbda,
#                                                td_delta.cpu()).to(self.device)
#         mu, std, probs = self.actor(states)
#         action_dists = torch.distributions.Normal(mu.detach(), std.detach())
#         # 动作是正态分布
        
#         old_log_probs = action_dists.log_prob(actions)

#         old_log_probs_2 = torch.log(probs.gather(1,actions_dis)).detach()

#         for _ in range(self.epochs):
#             mu,std,probs = self.actor(states)

#             # print(mu)
#             # print(std)


#             action_dists = torch.distributions.Normal(mu, std)

#             log_probs = action_dists.log_prob(actions)

#             log_probs_2 = torch.log(probs.gather(1,actions_dis))

#             ratio = torch.exp(log_probs - old_log_probs + log_probs_2 - old_log_probs_2)

#             # 看看
#             # print(ratio)

#             surr1 = ratio * advantage
#             surr2 = torch.clamp(ratio, 1 - self.eps, 1 + self.eps) * advantage
#             actor_loss = torch.mean(-torch.min(surr1, surr2))
#             critic_loss = torch.mean(
#                 F.mse_loss(self.critic(states), td_target.detach()))
#             self.actor_optimizer.zero_grad()
#             self.critic_optimizer.zero_grad()
#             actor_loss.backward()
#             critic_loss.backward()
#             self.actor_optimizer.step()
#             self.critic_optimizer.step()        





