import { useState } from 'react';
import Icon from '@/components/ui/icon';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

type View = 'feed' | 'profile' | 'friends' | 'messages' | 'communities' | 'notifications';

export default function Index() {
  const [currentView, setCurrentView] = useState<View>('feed');
  const [newPost, setNewPost] = useState('');

  const posts = [
    {
      id: 1,
      author: 'Анна Смирнова',
      avatar: 'АС',
      time: '2 часа назад',
      content: 'Только что вернулась с вечерней прогулки в парке! Осень — это волшебное время года 🍂',
      likes: 24,
      comments: 5,
      verified: true
    },
    {
      id: 2,
      author: 'Дмитрий Волков',
      avatar: 'ДВ',
      time: '4 часа назад',
      content: 'Запустили новый проект! Рад делиться с вами этой новостью. Долгая дорога привела к успеху! 🚀',
      likes: 48,
      comments: 12,
      verified: false
    },
    {
      id: 3,
      author: 'Елена Кузнецова',
      avatar: 'ЕК',
      time: '6 часов назад',
      content: 'Приготовила новый рецепт пасты с морепродуктами. Делюсь с вами! Скоро выложу подробности 👨‍🍳',
      likes: 67,
      comments: 18,
      verified: true
    }
  ];

  const friends = [
    { id: 1, name: 'Мария Петрова', mutual: 12, avatar: 'МП', online: true },
    { id: 2, name: 'Иван Сидоров', mutual: 8, avatar: 'ИС', online: false },
    { id: 3, name: 'Ольга Васильева', mutual: 15, avatar: 'ОВ', online: true },
    { id: 4, name: 'Сергей Морозов', mutual: 5, avatar: 'СМ', online: false }
  ];

  const communities = [
    { id: 1, name: 'Любители кофе', members: 2435, category: 'Кулинария', avatar: '☕' },
    { id: 2, name: 'Путешественники', members: 5821, category: 'Путешествия', avatar: '✈️' },
    { id: 3, name: 'Книжный клуб', members: 1204, category: 'Книги', avatar: '📚' },
    { id: 4, name: 'Фотография', members: 3567, category: 'Искусство', avatar: '📷' }
  ];

  const messages = [
    { id: 1, name: 'Анна Смирнова', lastMessage: 'Спасибо за поздравления!', time: '10 мин', unread: 2, avatar: 'АС' },
    { id: 2, name: 'Групповой чат "Проект"', lastMessage: 'Дмитрий: Завтра встреча в 10:00', time: '1 час', unread: 5, avatar: '👥' },
    { id: 3, name: 'Елена Кузнецова', lastMessage: 'Вы: Отлично, договорились!', time: '3 часа', unread: 0, avatar: 'ЕК' }
  ];

  const notifications = [
    { id: 1, type: 'like', text: 'Анна Смирнова оценила ваш пост', time: '5 мин назад' },
    { id: 2, type: 'comment', text: 'Дмитрий Волков прокомментировал ваше фото', time: '1 час назад' },
    { id: 3, type: 'friend', text: 'Мария Петрова добавила вас в друзья', time: '2 часа назад' },
    { id: 4, type: 'community', text: 'Новое событие в группе "Путешественники"', time: '3 часа назад' }
  ];

  const renderFeed = () => (
    <div className="space-y-6 animate-fade-in">
      <Card className="p-6">
        <div className="flex gap-4">
          <Avatar className="h-12 w-12">
            <AvatarFallback className="bg-primary text-primary-foreground">Вы</AvatarFallback>
          </Avatar>
          <div className="flex-1 space-y-3">
            <Textarea
              placeholder="Что у вас нового?"
              value={newPost}
              onChange={(e) => setNewPost(e.target.value)}
              className="min-h-[80px] resize-none"
            />
            <div className="flex justify-between items-center">
              <div className="flex gap-2">
                <Button variant="ghost" size="sm">
                  <Icon name="Image" className="h-4 w-4 mr-2" />
                  Фото
                </Button>
                <Button variant="ghost" size="sm">
                  <Icon name="Smile" className="h-4 w-4 mr-2" />
                  Эмодзи
                </Button>
              </div>
              <Button disabled={!newPost}>Опубликовать</Button>
            </div>
          </div>
        </div>
      </Card>

      {posts.map((post) => (
        <Card key={post.id} className="overflow-hidden hover:shadow-lg transition-shadow">
          <CardContent className="p-6">
            <div className="flex items-start gap-4">
              <Avatar className="h-12 w-12">
                <AvatarFallback className="bg-secondary text-secondary-foreground">{post.avatar}</AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold">{post.author}</h3>
                  {post.verified && (
                    <Badge variant="secondary" className="h-5 px-1.5">
                      <Icon name="BadgeCheck" className="h-3 w-3" />
                    </Badge>
                  )}
                  <span className="text-sm text-muted-foreground">• {post.time}</span>
                </div>
                <p className="mt-3 text-foreground leading-relaxed">{post.content}</p>
                <div className="flex gap-6 mt-4">
                  <Button variant="ghost" size="sm" className="gap-2">
                    <Icon name="Heart" className="h-4 w-4" />
                    {post.likes}
                  </Button>
                  <Button variant="ghost" size="sm" className="gap-2">
                    <Icon name="MessageCircle" className="h-4 w-4" />
                    {post.comments}
                  </Button>
                  <Button variant="ghost" size="sm" className="gap-2">
                    <Icon name="Share2" className="h-4 w-4" />
                    Поделиться
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );

  const renderProfile = () => (
    <div className="space-y-6 animate-fade-in">
      <Card className="overflow-hidden">
        <div className="h-32 bg-gradient-to-r from-primary/20 via-secondary/30 to-accent/20" />
        <CardContent className="relative pt-0 pb-6">
          <div className="flex flex-col sm:flex-row gap-6 -mt-16 sm:-mt-12">
            <Avatar className="h-32 w-32 border-4 border-background">
              <AvatarFallback className="bg-primary text-primary-foreground text-3xl">Вы</AvatarFallback>
            </Avatar>
            <div className="flex-1 mt-16 sm:mt-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-bold">Ваш Профиль</h2>
                  <p className="text-muted-foreground">@username</p>
                </div>
                <Button>
                  <Icon name="Settings" className="h-4 w-4 mr-2" />
                  Редактировать
                </Button>
              </div>
              <p className="mt-4 text-foreground">Здесь можно добавить описание вашего профиля, увлечений и интересов</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-3 gap-4">
        <Card className="p-6 text-center">
          <div className="text-3xl font-bold text-primary">248</div>
          <div className="text-sm text-muted-foreground mt-1">Друзей</div>
        </Card>
        <Card className="p-6 text-center">
          <div className="text-3xl font-bold text-primary">1,432</div>
          <div className="text-sm text-muted-foreground mt-1">Подписчиков</div>
        </Card>
        <Card className="p-6 text-center">
          <div className="text-3xl font-bold text-primary">87</div>
          <div className="text-sm text-muted-foreground mt-1">Публикаций</div>
        </Card>
      </div>

      <Card className="p-6">
        <h3 className="font-semibold text-lg mb-4">Интересы</h3>
        <div className="flex flex-wrap gap-2">
          {['Фотография', 'Путешествия', 'Кулинария', 'Книги', 'Спорт', 'Музыка'].map((interest) => (
            <Badge key={interest} variant="secondary" className="px-3 py-1">
              {interest}
            </Badge>
          ))}
        </div>
      </Card>
    </div>
  );

  const renderFriends = () => (
    <div className="space-y-6 animate-fade-in">
      <Card className="p-6">
        <div className="flex gap-2">
          <Input placeholder="Поиск друзей..." className="flex-1" />
          <Button>
            <Icon name="Search" className="h-4 w-4" />
          </Button>
        </div>
      </Card>

      <div>
        <h3 className="text-lg font-semibold mb-4">Рекомендации</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {friends.map((friend) => (
            <Card key={friend.id} className="p-6">
              <div className="flex items-center gap-4">
                <div className="relative">
                  <Avatar className="h-16 w-16">
                    <AvatarFallback className="bg-secondary text-secondary-foreground">{friend.avatar}</AvatarFallback>
                  </Avatar>
                  {friend.online && (
                    <div className="absolute bottom-0 right-0 h-4 w-4 bg-green-500 rounded-full border-2 border-background" />
                  )}
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold">{friend.name}</h4>
                  <p className="text-sm text-muted-foreground">{friend.mutual} общих друзей</p>
                </div>
                <Button size="sm">
                  <Icon name="UserPlus" className="h-4 w-4 mr-2" />
                  Добавить
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );

  const renderMessages = () => (
    <div className="space-y-6 animate-fade-in">
      <Card className="p-6">
        <Tabs defaultValue="all" className="w-full">
          <TabsList className="w-full">
            <TabsTrigger value="all" className="flex-1">Все сообщения</TabsTrigger>
            <TabsTrigger value="unread" className="flex-1">Непрочитанные</TabsTrigger>
          </TabsList>
          <TabsContent value="all" className="mt-6">
            <div className="space-y-3">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className="flex items-center gap-4 p-4 rounded-lg hover:bg-muted/50 transition-colors cursor-pointer"
                >
                  <Avatar className="h-12 w-12">
                    <AvatarFallback className="bg-secondary text-secondary-foreground">{message.avatar}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-2">
                      <h4 className="font-semibold truncate">{message.name}</h4>
                      <span className="text-xs text-muted-foreground whitespace-nowrap">{message.time}</span>
                    </div>
                    <p className="text-sm text-muted-foreground truncate">{message.lastMessage}</p>
                  </div>
                  {message.unread > 0 && (
                    <Badge className="bg-primary text-primary-foreground">{message.unread}</Badge>
                  )}
                </div>
              ))}
            </div>
          </TabsContent>
          <TabsContent value="unread" className="mt-6">
            <div className="text-center py-8 text-muted-foreground">
              У вас {messages.filter(m => m.unread > 0).length} непрочитанных диалога
            </div>
          </TabsContent>
        </Tabs>
      </Card>
    </div>
  );

  const renderCommunities = () => (
    <div className="space-y-6 animate-fade-in">
      <Card className="p-6">
        <div className="flex gap-2">
          <Input placeholder="Поиск сообществ..." className="flex-1" />
          <Button>Создать</Button>
        </div>
      </Card>

      <div>
        <h3 className="text-lg font-semibold mb-4">Популярные сообщества</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {communities.map((community) => (
            <Card key={community.id} className="p-6">
              <div className="flex items-start gap-4">
                <div className="text-4xl">{community.avatar}</div>
                <div className="flex-1">
                  <h4 className="font-semibold">{community.name}</h4>
                  <Badge variant="outline" className="mt-1 mb-2">
                    {community.category}
                  </Badge>
                  <p className="text-sm text-muted-foreground">{community.members.toLocaleString()} участников</p>
                  <Button size="sm" className="mt-3 w-full">
                    Вступить
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );

  const renderNotifications = () => (
    <div className="space-y-4 animate-fade-in">
      <Card className="p-6">
        <h3 className="font-semibold text-lg mb-4">Уведомления</h3>
        <ScrollArea className="h-[600px]">
          <div className="space-y-3">
            {notifications.map((notif) => (
              <div
                key={notif.id}
                className="flex items-start gap-4 p-4 rounded-lg hover:bg-muted/50 transition-colors cursor-pointer"
              >
                <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                  {notif.type === 'like' && <Icon name="Heart" className="h-5 w-5 text-primary" />}
                  {notif.type === 'comment' && <Icon name="MessageCircle" className="h-5 w-5 text-primary" />}
                  {notif.type === 'friend' && <Icon name="UserPlus" className="h-5 w-5 text-primary" />}
                  {notif.type === 'community' && <Icon name="Users" className="h-5 w-5 text-primary" />}
                </div>
                <div className="flex-1">
                  <p className="text-sm">{notif.text}</p>
                  <p className="text-xs text-muted-foreground mt-1">{notif.time}</p>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </Card>
    </div>
  );

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <h1 className="text-2xl font-bold text-primary">Вместе</h1>
            <nav className="hidden md:flex gap-1">
              <Button
                variant={currentView === 'feed' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('feed')}
              >
                <Icon name="Home" className="h-4 w-4 mr-2" />
                Лента
              </Button>
              <Button
                variant={currentView === 'profile' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('profile')}
              >
                <Icon name="User" className="h-4 w-4 mr-2" />
                Профиль
              </Button>
              <Button
                variant={currentView === 'friends' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('friends')}
              >
                <Icon name="Users" className="h-4 w-4 mr-2" />
                Друзья
              </Button>
              <Button
                variant={currentView === 'messages' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('messages')}
              >
                <Icon name="MessageSquare" className="h-4 w-4 mr-2" />
                Сообщения
              </Button>
              <Button
                variant={currentView === 'communities' ? 'default' : 'ghost'}
                onClick={() => setCurrentView('communities')}
              >
                <Icon name="Users" className="h-4 w-4 mr-2" />
                Сообщества
              </Button>
            </nav>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              className="relative"
              onClick={() => setCurrentView('notifications')}
            >
              <Icon name="Bell" className="h-5 w-5" />
              <span className="absolute top-1 right-1 h-2 w-2 bg-primary rounded-full" />
            </Button>
            <Button variant="ghost" size="icon">
              <Icon name="Search" className="h-5 w-5" />
            </Button>
            <Avatar className="h-9 w-9 cursor-pointer">
              <AvatarFallback className="bg-primary text-primary-foreground">Вы</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {currentView === 'feed' && renderFeed()}
        {currentView === 'profile' && renderProfile()}
        {currentView === 'friends' && renderFriends()}
        {currentView === 'messages' && renderMessages()}
        {currentView === 'communities' && renderCommunities()}
        {currentView === 'notifications' && renderNotifications()}
      </main>

      <nav className="md:hidden fixed bottom-0 left-0 right-0 border-t bg-background/95 backdrop-blur">
        <div className="flex justify-around p-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCurrentView('feed')}
            className={currentView === 'feed' ? 'text-primary' : ''}
          >
            <Icon name="Home" className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCurrentView('friends')}
            className={currentView === 'friends' ? 'text-primary' : ''}
          >
            <Icon name="Users" className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCurrentView('messages')}
            className={currentView === 'messages' ? 'text-primary' : ''}
          >
            <Icon name="MessageSquare" className="h-5 w-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCurrentView('profile')}
            className={currentView === 'profile' ? 'text-primary' : ''}
          >
            <Icon name="User" className="h-5 w-5" />
          </Button>
        </div>
      </nav>
    </div>
  );
}