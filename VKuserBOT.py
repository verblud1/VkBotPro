import vk_api
import sys
import time

class vkBot():

    def __init__(self):
        self.accs= self.load_accs()
        self.check = self.check()
        self.user_id = []
        
        self.input = self.input()
        

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
                ada = d.account.getProfileInfo() 
                amountAcc.append(i)       
            except vk_api.exceptions.ApiError:
                ada = d.account.getProfileInfo()
                print('Неверный access_token. Возможно, аккаунт забанен, array =','[ id:',ada['id'],']')
        
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



    def mes(self):
        ha = 1
        try:

            d = input('делаем в цикле?(y/n): ')
            iu = int(input('кому отправляем?(id): '))
            mes = input('введите сообщение: ')

            if d == 'y':
                ha = int(input('сколько циклов?: '))

        except:
            print('ОШИБКА! Нужно число.')

        g = 0
        while(g!=ha):
            g+=1
            for i in self.check:
                try:
                    d = vk_api.VkApi(token=i).get_api()
                    d.messages.send(user_id=iu,message=mes,random_id=0)
                    ada = d.account.getProfileInfo()
                    print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] отправил сообщение')
                except vk_api.exceptions.ApiError: 
                    ada = d.account.getProfileInfo()
                    print('сообщение не отправлено. Вероятно, проблемы с капчей или у пользователя закрыты сообщения, array =','[ id:',ada['id'],']')
                   

    def inf(self):
        try:
            use = int(input('id пользователя: '))
        except:
            print('нужно число!')
            self.inf()
        try:
            for i in self.check:
                d = vk_api.VkApi(token=i[0]).get_api()
                infoUser = d.users.get(user_id = use)
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
                    ada = d.account.getProfileInfo()
                    print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] поставил лайк')
                except vk_api.exceptions.ApiError:    
                        try:
                            d = vk_api.VkApi(token=i).get_api()
                            ada = d.account.getProfileInfo()
                            d.likes.add(type = 'photo',owner_id = user_id,item_id = post_id)
                            print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] поставил лайк')
                        except vk_api.exceptions.ApiError: 
                            ada = d.account.getProfileInfo()
                            print('невозможно поставить лайк. Вероятно, проблемы с капчей, array =','[ id:',ada['id'],']') 

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
                ada = d.account.getProfileInfo()
                print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] опубликовал запись')
            except vk_api.exceptions.ApiError: 
                ada = d.account.getProfileInfo()
                print('невозможно опубликовать запись. Вероятно, у пользователя закрыта стена, array =', '[ id:',ada['id'],']')


        

    def wall(self):
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
                    ada = d.account.getProfileInfo()
                    print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] оставил комментарий')
                except vk_api.exceptions.ApiError: 
                    try:
                        d = vk_api.VkApi(token=i).get_api()
                        d.video.createComment(owner_id = owner_id,video_id = el_id,message = message)
                        ada = d.account.getProfileInfo()
                        print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] оставил комментарий')
                    except vk_api.exceptions.ApiError:
                        try:
                            d = vk_api.VkApi(token=i).get_api()
                            d.photos.createComment(owner_id = owner_id,photo_id = el_id,message = message)
                            ada = d.account.getProfileInfo()
                            print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] оставил комментарий')
                        except vk_api.exceptions.ApiError:
                            ada = d.account.getProfileInfo()
                            print('невозможно оставить коммент. Возможно, у поста закрыты комментарии, array =','[ id:',ada['id'],']')

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
                    ada = d.account.getProfileInfo()
                    print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] вступил в группу')
                except vk_api.exceptions.ApiError:
                    ada = d.account.getProfileInfo()
                    print('акк не смог вступить в группу, array = ','[ id:',ada['id'],']')
       

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
                ada = d.account.getProfileInfo()
                print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] добавился в друзья')
            except vk_api.exceptions.ApiError:
                ada = d.account.getProfileInfo()
                print('акк не смог добавиться в друзья, array =', '[ id:',ada['id'],']')
        
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
                        ada = d.account.getProfileInfo()
                        print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] вступил в группу', gr)
                    except Exception as e:
                        ada = d.account.getProfileInfo()
                        print(e,'| акк не смог вступить в группу, array = ','[ id acc:',ada['id'], 'id group:',gr, ']')

        return self.group_id
    
    def input(self):
        print('h - справка по модам, re - реконнект акков')
        
        a = input('>>')
        if a == 'h':
            self.help()

        if a == '0':
            self.load_group()
        if a == '1':
            self.mes()
        if a == '2':
            self.wall()
        if a == '3':
            self.like()
        if a == '4':
            self.inf()
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

