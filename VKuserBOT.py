import vk_api
import sys

class vkBot():

    def __init__(self):
        self.accs= self.load_accs()
        self.check = self.check()
        self.user_id = []
        
        self.input = self.input()
        
#start

    def load_accs(self):   
            tok = []
            self.user_id = []

            file = open(sys.path[0] + '/tokenVK.txt', 'r',encoding = 'utf-8-sig').readlines()
            for q in file:
            
                try:
                    q = q.strip()
                    tmp = q.split(':',1)
                    self.user_id.append(tmp[0])
                    tok.append([bytes(tmp[1].strip(), 'UTF-8') ])
                    print('загружен', tmp[0])
                except Exception as e:
                    print(e,'не удалось загрузить аккаунт, array=',tmp)
                
            
            return tok 


    def check(self):
        amountAcc=[]
        for i in self.accs:
            
            try:
                d = vk_api.VkApi(token=i).get_api()
                d.account.getInfo(fields = 'country')
                amountAcc.append(i)       
            except Exception as e:
                print('Неверный access_token. Возможно, аккаунт забанен, array =','[ Access_token:',i,']',e)
        
        print('загружено', len(amountAcc), 'аккаунтов')
        return amountAcc

    def help(self):
        print('''
    моды:
    0 - массовое вступление в группы из group_list.txt со всех акков
    1 - отправка сообщений
    2 - комментирование записей
    3 - поставить лайк
    4 - инфа о акке
    5 - оставление записей на стене
    6 - вступление в группу
    7 - добавление в друзья
    q - выход
        ''')


#main

    def mes(self):
        cycle_count = 1
        try:

            d = input('делаем в цикле?(y/n): ')
            user_id = int(input('кому отправляем?(id): '))
            mes = input('введите сообщение: ')

            if d == 'y':
                cycle_count = int(input('сколько циклов?: '))

        except:
            print('ОШИБКА! Нужно число.')

        g = 0
        while(g!=cycle_count):
            g+=1
            for i in self.check:
                try:
                    d = vk_api.VkApi(token=i).get_api()
                    d.messages.send(user_id=user_id,message=mes,random_id=0)
                    u_info = d.account.getProfileInfo()
                    print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] отправил сообщение')
                except vk_api.exceptions.ApiError: 
                    u_info = d.account.getProfileInfo()
                    print('сообщение не отправлено. Вероятно, проблемы с капчей или у пользователя закрыты сообщения, array =','[ id:',u_info['id'],']')
                   

    def info_user(self):
        try:
            use = int(input('id пользователя: '))
        except:
            print('нужно число!')
            self.inf()
        try:
            for i in self.check:
                d = vk_api.VkApi(token=i[0]).get_api()
                infoUser = d.users.get(user_id = use, fields='city,country,about,nickname,personal,maiden_name,status,contacts,domain,friend_status,has_mobile,followers_count,screen_name,wall_default,verified')
            print(infoUser)
        except Exception as e:
            print(e)


    def like(self):
        try:
            user_id = int(input('id кого лайкаем: '))
            post_id = int(input('id записи: '))
        except:
            print('нужно число!')
            self.like()
        try:
            for i in self.check:
                try:
                    d = vk_api.VkApi(token=i).get_api()
                    d.likes.add(type = 'comment',owner_id = user_id,item_id = post_id)
                    u_info = d.account.getProfileInfo()
                    print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] поставил лайк')
                except vk_api.exceptions.ApiError:    
                        try:
                            d = vk_api.VkApi(token=i).get_api()
                            u_info = d.account.getProfileInfo()
                            d.likes.add(type = 'photo',owner_id = user_id,item_id = post_id)
                            print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] поставил лайк')
                        except vk_api.exceptions.ApiError: 
                            u_info = d.account.getProfileInfo()
                            print('невозможно поставить лайк. Вероятно, проблемы с капчей, array =','[ id:',u_info['id'],']') 
        except:
            pass  
        
    def post(self):
        try:
            owner_id = int(input('id у кого публикуем: '))
            message = input('публикуемый текст: ')
        except:
            print('нужно число!')
            self.post()
    
        for i in self.check:
            try:
                d = vk_api.VkApi(token=i).get_api()
                d.wall.post(owner_id = owner_id,message=message)
                u_info = d.account.getProfileInfo()
                print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] опубликовал запись')
            except vk_api.exceptions.ApiError: 
                u_info = d.account.getProfileInfo()
                print('невозможно опубликовать запись. Вероятно, у пользователя закрыта стена, array =', '[ id:',u_info['id'],']')

    def wall_comment(self):
        try:
            owner_id = int(input('кого комментим?(id):'))
            el_id = int(input('id поста:'))
            message = input('cообщение:')
        except:
            print('нужно число!')
            return self.wall()
        try:
            for i in self.check:
                try:
                    d = vk_api.VkApi(token=i).get_api()
                    d.wall.createComment(owner_id = owner_id,post_id = el_id, message = message )
                    u_info = d.account.getProfileInfo()
                    print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] оставил комментарий')
                except vk_api.exceptions.ApiError: 
                    try:
                        d = vk_api.VkApi(token=i).get_api()
                        d.video.createComment(owner_id = owner_id,video_id = el_id,message = message)
                        u_info = d.account.getProfileInfo()
                        print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] оставил комментарий')
                    except vk_api.exceptions.ApiError:
                        try:
                            d = vk_api.VkApi(token=i).get_api()
                            d.photos.createComment(owner_id = owner_id,photo_id = el_id,message = message)
                            u_info = d.account.getProfileInfo()
                            print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] оставил комментарий')
                        except vk_api.exceptions.ApiError:
                            u_info = d.account.getProfileInfo()
                            print('невозможно оставить коммент. Возможно, у поста закрыты комментарии, array =','[ id:',u_info['id'],']')
        except:
            pass

        
    def group(self):
        try:
            group_id = int(input('id группы: '))
        except:
            print('Нужно число!')
            self.group()
        for i in self.check:
                try:
                    d = vk_api.VkApi(token=i).get_api()
                    d.groups.join(group_id = group_id)
                    u_info = d.account.getProfileInfo()
                    print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] вступил в группу')
                except vk_api.exceptions.ApiError:
                    u_info = d.account.getProfileInfo()
                    print('акк не смог вступить в группу, array = ','[ id:',u_info['id'],']')
       

    def friends_add(self):
        try:
            user_id = int(input('id пользователя: '))
        except:
            print('нужно число!')
            self.friends_add()
        for i in self.check:
            try:
                d = vk_api.VkApi(token=i).get_api()
                d.friends.add(user_id = user_id)
                u_info = d.account.getProfileInfo()
                print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] добавился в друзья')
            except vk_api.exceptions.ApiError:
                u_info = d.account.getProfileInfo()
                print('акк не смог добавиться в друзья, array =', '[ id:',u_info['id'],']')


    #load group from file 

    def load_group(self):
        self.group_id = []

        file = open(sys.path[0] + '/group_list.txt', 'r',encoding = 'utf-8-sig').readlines()
        for q in file:
            try:
                q = q.strip()
                tmp = q.split()
                self.group_id.append(int(tmp[0]))
                print('загружена группа ',q)
            except Exception as e:
                print(e,'не удалось загрузить группу, array=',tmp)
        print('загружено', len(self.group_id), 'групп')

        for gr in self.group_id:
            for i in self.check:
                    try:
                        d = vk_api.VkApi(token=i).get_api()
                        d.groups.join(group_id = gr)
                        u_info = d.account.getProfileInfo()
                        print(u_info['first_name'],u_info['last_name'],'[ id:',u_info['id'],'] вступил в группу', gr)
                    except Exception as e:
                        u_info = d.account.getProfileInfo()
                        print(e,'| акк не смог вступить в группу, array = ','[ id acc:',u_info['id'], 'id group:',gr, ']')

        return self.group_id
    
 

    
    def input(self):
        print('h - справка по модам, re - реконнект акков, q - выход')
        
        a = input('>>')
        if a == 'h':
            self.help()

        if a == '0':
            self.load_group()
        if a == '1':
            self.mes()
        if a == '2':
            self.wall_comment()
        if a == '3':
            self.like()
        if a == '4':
            self.info_user()
        if a == '5':
            self.post()
        if a == '6':
            self.group()
        if a == '7':
            self.friends_add()
        
        if a == 're':   
            vkBot()
        if a == 'q':
            exit(0)
        else:
            self.input()
    
    
    print('')
    

if __name__ == '__main__':
    main = vkBot()
    exit()
