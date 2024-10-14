from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    website_link = db.Column(db.String(120))

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    website_link = db.Column(db.String(120))


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)

    def __repr__(self):
        return f'<Show {self.id}, date: {self.date}, artist_id: {self.artist_id}, venue_id: {self.venue_id}>'

## Create data in database
def seed_data():
    # Check if the database is empty
    if Venue.query.count() == 0 and Artist.query.count() == 0:
        # Add Venues
        venue1 = Venue(
            name="The Musical Hop",
            city="San Francisco",
            state="CA",
            address="1015 Folsom Street",
            phone="123-123-1234",
            image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60",
            facebook_link="https://www.facebook.com/TheMusicalHop",
        )

        venue2 = Venue(
            name="The Dueling Pianos Bar",
            city="New York",
            state="NY",
            address="335 Delancey Street",
            phone="914-003-1132",
            image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=750&q=80",
            facebook_link="https://www.facebook.com/theduelingpianos",
        )

        venue3 = Venue(
            name="Nhà Hát Lớn Hà Nội",
            city="Hà Nội",
            state="HN",
            address="1 Tràng Tiền, Hoàn Kiếm",
            phone="024-3825-2251",
            image_link="https://images.unsplash.com/photo-1542077338-9e67a6d4c22d?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60",
            facebook_link="https://www.facebook.com/nhahatlonhanoi",
        )

        venue4 = Venue(
            name="Cà Phê Nhạc Trẻ",
            city="TP Hồ Chí Minh",
            state="HCM",
            address="123 Lê Lợi, Bến Nghé",
            phone="028-3822-1188",
            image_link="https://images.unsplash.com/photo-1543515696-6c9a8e5757b5?ixlib=rb-1.2.1&auto=format&fit=crop&w=750&q=80",
            facebook_link="https://www.facebook.com/caphethanhpho",
        )

        venue5 = Venue(
            name="Nhà Hát Thành Phố",
            city="TP Hồ Chí Minh",
            state="HCM",
            address="7 Công trường Lam Sơn, Bến Nghé",
            phone="028-3823-3009",
            image_link="https://images.unsplash.com/photo-1547033051-7d13d8c7a6e0?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60",
            facebook_link="https://www.facebook.com/nhahatthanhpho",
        )

        venue6 = Venue(
            name="Trung Tâm Hội Nghị Ariyana",
            city="Đà Nẵng",
            state="DN",
            address="98 Võ Nguyên Giáp, Ngũ Hành Sơn",
            phone="0236-3983-333",
            image_link="https://images.unsplash.com/photo-1566227791450-bb441de14cda?ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60",
            facebook_link="https://www.facebook.com/ariyanaconvention",
        )


        db.session.add(venue1)
        db.session.add(venue2)
        db.session.add(venue3)
        db.session.add(venue4)
        db.session.add(venue5)
        db.session.add(venue6)

        # Add Artists
        artist1 = Artist(
            name="Guns N Petals",
            city="San Francisco",
            state="CA",
            phone="326-123-5000",
            genres="Rock n Roll",
            image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
            facebook_link="https://www.facebook.com/GunsNPetals",
        )

        artist2 = Artist(
            name="Matt Quevedo",
            city="New York",
            state="NY",
            phone="300-400-5000",
            genres="Jazz",
            image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&auto=format&fit=crop&w=334&q=80",
            facebook_link="https://www.facebook.com/mattquevedo923251523",
        )
        artist3 = Artist(
            name="Bích Phương",
            city="Hà Nội",
            state="HN",
            phone="090-123-4567",
            genres="Pop",
            image_link="https://images.unsplash.com/photo-1529276863937-62f1f8b8c8e8?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
            facebook_link="https://www.facebook.com/bichphuong",
        )

        artist4 = Artist(
            name="Sơn Tùng M-TP",
            city="TP Hồ Chí Minh",
            state="HCM",
            phone="091-234-5678",
            genres="Hip Hop",
            image_link="https://images.unsplash.com/photo-1584328495154-dc07d964a3a8?ixlib=rb-1.2.1&auto=format&fit=crop&w=334&q=80",
            facebook_link="https://www.facebook.com/son.tungmtp",
        )

        artist5 = Artist(
            name="Tóc Tiên",
            city="TP Hồ Chí Minh",
            state="HCM",
            phone="093-456-7890",
            genres="R&B",
            image_link="https://images.unsplash.com/photo-1547721064-5b1a17b5b5d2?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
            facebook_link="https://www.facebook.com/tactien",
        )

        artist6 = Artist(
            name="Hương Tràm",
            city="Hà Nội",
            state="HN",
            phone="097-654-3210",
            genres="Ballad",
            image_link="https://images.unsplash.com/photo-1518110970847-bb4a51dfac12?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80",
            facebook_link="https://www.facebook.com/huongtramofficial",
        )


        db.session.add(artist1)
        db.session.add(artist2)
        db.session.add(artist3)
        db.session.add(artist4)
        db.session.add(artist5)
        db.session.add(artist6)

        # Commit the session
        db.session.commit()

        # Add show
        show1 = Show(
            date = "2024/10/01",
            artist_id = 1,
            venue_id = 2
        )

        show2 = Show(
            date = "2024/09/10",
            artist_id = 3,
            venue_id = 4
        )

        show3 = Show(
            date = "2024/08/10",
            artist_id = 1,
            venue_id = 5
        )

        db.session.add(show1)
        db.session.add(show2)
        db.session.add(show3)

        db.session.commit()
