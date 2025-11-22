import mimetypes
import os

from database import Database
from error import HTTPError
from floot import Floot
from floot_comment import FlootComment
from response import Response

SERVER_SRC_DIR = os.path.dirname(os.path.realpath(__file__))
CLIENT_SRC_DIR = os.path.abspath(os.path.join(SERVER_SRC_DIR, "..", "client"))

db = Database()


# GET /
def serve_file(path):
    """
    Returns a static file from the client/ directory. This is used to send
    files like index.html, flutterer.js, style.css, etc. to the client.

    You don't need to understand or modify this function.
    """
    if not path or path == "/":
        path = "/index.html"
    target_file_path = os.path.abspath(os.path.join(CLIENT_SRC_DIR, path[1:]))
    # Avoid serving files above client source directory for security
    if not target_file_path.startswith(CLIENT_SRC_DIR + os.sep) or not os.path.isfile(
        target_file_path
    ):
        return HTTPError(404, "File not found")

    with open(target_file_path, "rb") as f:
        # Return the file. Guess the content-type based on the file extension
        # (e.g. a .html file is probably text/html).
        return Response(
            f.read(), content_type=mimetypes.guess_type(target_file_path)[0]
        )


# GET /api/floots
def get_floots():
    """
    Returns a list of all floots from the database. Remember that these
    functions are used to send JSON to the client, so you should return a list
    of dictionaries, *not* a list of Floot objects. (Lists and dictionaries are
    easily converted to JSON so that the client can understand them, but it's
    not straightforward to send an arbitrary object, like a Floot object, over
    the internet.) You may find the Floot to_dictionary() method helpful.
    """
    floots = db.get_floots()
    res = []
    for floot in floots:
        res.append(floot.to_dictionary())
    return res


# GET /api/floots/{floot_id}
def get_floot(floot_id):
    """
    Given a floot ID, returns the floot if that ID exists in the database, or
    returns an HTTPError with status 404 if the provided ID could not be found.
    You should return the floot as a dictionary, not as a Floot object (see
    Floot.to_dictionary()).
    """
    if db.has_floot(floot_id):
        return db.get_floot_by_id(floot_id).to_dictionary()
    else:
        return HTTPError(404, f"No floot with id {floot_id} in database")


# POST /api/floots
def create_floot(request_body):
    """
    Creates a new floot from the payload information in request_body, which is
    a dict that should have the following shape:
    {
        "message": "contents of floot...",
        "username": "name of user",
    }

    We don't have user-signups on this super simple system, so you can assume
    that any username is valid, and any message is valid. However, if the
    "message" or "username" keys are missing from request_body (which is
    possible; the client might make a mistake and not send them), you should
    return an HTTPError with status 400.

    When you've saved the new floot to the database, return the floot as a
    dictionary (see Floot.to_dictionary).
    """
    if "message" in request_body and "username" in request_body:
        floot = Floot(request_body["message"], request_body["username"])
        db.save_floot(floot)
        return floot.to_dictionary()
    else:
        return HTTPError(400, "Missing keys in payload")


# POST /api/floots/{floot_id}/delete
def delete_floot(floot_id, request_body):
    """
    Given a floot_id and request_body with the following shape:
    {
        "username": "string",
    }
    Deletes the specified floot from the database if the user making the
    request posted that floot.

    * If floot_id is invalid, this function should return an HTTPError with a
      status of 404.
    * If the "username" key is missing from request_body, this function should
      return an HTTPError with a status of 400.
    * If the user making this request (as specified in request_body) is not the
      user that posted the floot, this function should return an HTTPError with
      a status of 401.
    * If everything worked fine and the floot was successfully deleted, this
      function should return "OK".
    """
    if not db.has_floot(floot_id):
        return HTTPError(404, f"No floot with id {floot_id} in database")
    elif "username" not in request_body:
        return HTTPError(400, "Missing keys in payload")
    elif request_body["username"] != db.get_floot_by_id(floot_id).get_username():
        return HTTPError(
            401, "Provided username does not match with the one who created the floot"
        )
    else:
        try:
            db.delete_floot_by_id(floot_id)
            return "OK"
        except:
            return HTTPError(404, f"No floot with id {floot_id} in database")


# GET /api/floot/{floot_id}/comments
def get_comments(floot_id):
    """
    Given a floot_id, returns a list of comments for that floot. (You should
    return a list of dictionaries, not a list of FlootComment objects.) If
    floot_id is invalid, return an HTTPError with status 404.
    """
    if db.has_floot(floot_id):
        comment_list = db.get_floot_by_id(floot_id).get_comments()
        res = []
        for comment in comment_list:
            res.append(comment.to_dictionary())
        return res
    else:
        return HTTPError(404, f"No floot with id {floot_id} in database")


# POST /api/floots/{floot_id}/comments
def create_comment(floot_id, request_body):
    """
    Takes a floot ID and request_body with the following shape: {
        "username": "string",
        "message": "contents of comment",
    }
    Creates and saves a new comment under the specified floot. If floot_id is
    invalid, returns an HTTPError with status 404. If the "username" or
    "message" keys are missing from request_body, returns an HTTPError with
    status 400. Otherwise, if the comment was created successfully, returns the
    new comment as a dictionary (see FlootComment.to_dictionary()).
    """
    if not db.has_floot(floot_id):
        return HTTPError(404, f"No floot with id {floot_id} in database")
    elif "username" not in request_body or "message" not in request_body:
        return HTTPError(400, "Missing keys in payload")
    else:
        floot = db.get_floot_by_id(floot_id)
        comment = FlootComment(request_body["message"], request_body["username"])
        try:
            floot.create_comment(comment)
            return comment.to_dictionary()
        except:
            return HTTPError(400, "Comment crreation failed")


# POST /api/floots/{floot_id}/comments/{comment_id}/delete
def delete_comment(floot_id, comment_id, request_body):
    """
    Takes a floot ID and a comment ID; the request_body payload is of the
    following shape:
    {
        "username": "string",
    }
    Removes the specified comment from the specified floot.

    * If floot_id is invalid, return an HTTPError with status 404.
    * If comment_id does not exist in the specified floot, return an HTTPError
      with status 404 as well.
    * If the "username" key is missing from the request_body dict, return an
      HTTPError with status 400.
    * If the user specified in request_body is not allowed to delete the comment
      (because they're not the author of the comment), return an HTTPError with
      status 401.
    * Otherwise, if everything works successfully, return "OK".
    """
    if not db.has_floot(floot_id):
        return HTTPError(404, f"No floot with id {floot_id} in database")

    if "username" not in request_body:
        return HTTPError(400, "Missing keys in payload")

    floot = db.get_floot_by_id(floot_id)
    comments = floot.get_comments()

    if get_comment_by_id(comments, comment_id) is None:
        return HTTPError(404, f"No floot comment with id {comment_id} in database")

    comment_to_delete = get_comment_by_id(comments, comment_id)

    if request_body["username"] != comment_to_delete.get_author():
        return HTTPError(
            401, f"{request_body['username']} is not the author for the comment"
        )
    else:
        try:
            floot.delete_comment(comment_to_delete, request_body["username"])
            return "OK"
        except:
            return HTTPError(400, "Comment deletion failed")


# POST /api/floots/{floot_id}/like
def like_floot(floot_id, request_body):
    """
    OPTIONAL: This function is not required, but you can implement it if you
    want to add "like/heart button" functionality.

    Shape of request_body:
    {
        "username": "string",
    }

    Sets a Floot as liked by a given username (see Floot.set_liked()). Repeat
    requests from the same user liking the same floot have no effect (the like
    count should not increase). If floot_id is invalid, you should return an
    HTTPError with status 404, and if "username" is missing from request_body,
    return an HTTPError with status 401.
    """
    if not db.has_floot(floot_id):
        return HTTPError(404, f"No floot with id {floot_id} in database")

    if "username" not in request_body:
        return HTTPError(400, "Missing keys in payload")

    floot = db.get_floot_by_id(floot_id)
    liked_by = floot.get_liked_by()

    if request_body["username"] in liked_by:
        return

    floot.set_liked(request_body["username"], True)
    return "OK"


# POST /api/floots/{floot_id}/unlike
def unlike_floot(floot_id, request_body):
    """
    OPTIONAL: This function is not required, but you can implement it if you
    want to add "like/heart button" functionality.

    Shape of request_body:
    {
        "username": "string",
    }

    Sets a Floot as *not liked* by a given username (see Floot.set_liked()).
    If the specified user had not already liked this floot, this has no effect
    (but doesn't return an error either).  If floot_id is invalid, you should
    return an HTTPError with status 404, and if "username" is missing from
    request_body, return an HTTPError with status 401.
    """
    if not db.has_floot(floot_id):
        return HTTPError(404, f"No floot with id {floot_id} in database")

    if "username" not in request_body:
        return HTTPError(400, "Missing keys in payload")

    floot = db.get_floot_by_id(floot_id)
    liked_by = floot.get_liked_by()

    if request_body["username"] not in liked_by:
        return

    floot.set_liked(request_body["username"], False)
    return "OK"


# This specifies which functions should be called given a particular incoming
# path. You don't need to understand or change this, unless you're doing an
# extension that requires adding new API routes.
GET_ROUTES = [
    ("/api/floots", get_floots),
    (("/api/floots/(.*?)/comments", "floot_id"), get_comments),
    (("/api/floots/(.*)", "floot_id"), get_floot),
    (("(/.*)", "path"), serve_file),
]

# This specifies which functions should be called given a particular incoming
# path. You don't need to understand or change this, unless you're doing an
# extension that requires adding new API routes.
POST_ROUTES = [
    (("/api/floots"), create_floot),
    (("/api/floots/(.*?)/comments", "floot_id"), create_comment),
    (
        ("/api/floots/(.*?)/comments/(.*)/delete", "floot_id", "comment_id"),
        delete_comment,
    ),
    (("/api/floots/(.*)/delete", "floot_id"), delete_floot),
    (("/api/floots/(.*)/like", "floot_id"), like_floot),
    (("/api/floots/(.*)/unlike", "floot_id"), unlike_floot),
]

# HELPERS
# -------


# Return the FlootComment() Object if a comment_id exists in a given list.
# Otherwise return None.
def get_comment_by_id(
    comments: list[FlootComment], comment_id: str
) -> FlootComment | None:
    for comment in comments:
        if comment_id == comment.get_id():
            return comment
    return None
