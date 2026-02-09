from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from datetime import datetime

db = SQLAlchemy()

# =====================================================
# USER TABLE
# =====================================================
class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)

    # Relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

# =====================================================
# PLANET TABLE
# =====================================================
class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    characters: Mapped[list["Character"]] = relationship(back_populates="homeworld")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

    def __repr__(self):
        return f"<Planet {self.name}>"

# =====================================================
# CHARACTER TABLE
# =====================================================
class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    species: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    # Relationships
    homeworld: Mapped["Planet"] = relationship(back_populates="characters")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="character")

    def __repr__(self):
        return f"<Character {self.name}>"

# =====================================================
# FAVORITE TABLE (User saves favorites)
# =====================================================
class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int | None] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int | None] = mapped_column(ForeignKey("planet.id"), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped["Character | None"] = relationship(back_populates="favorites")
    planet: Mapped["Planet | None"] = relationship(back_populates="favorites")

    def __repr__(self):
        return f"<Favorite user={self.user_id}>"

# =====================================================
# POST TABLE (BLOG POSTS)
# =====================================================
class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relationships
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")

    def __repr__(self):
        return f"<Post {self.title}>"

# =====================================================
# COMMENT TABLE
# =====================================================
class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def __repr__(self):
        return f"<Comment by user {self.user_id}>"