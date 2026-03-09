Adding **Dynamic Scaling** is a great way to handle the "Cozy" progression. It ensures the early game feels manageable and short, while the late game rewards your upgraded **Ink Reservoir** with massive, sprawling ruins to get lost in.

Here is your updated roadmap:

### 🛠️ Priority 1: The Meta-Loop (Town)

* **Implement the Ink Foundry:** Create the interaction logic to trade Gold for a full Ink refill.
* **Build the Drafting Shack Menu:** "Sell" your map to clear `mapped_data` and trigger a fresh seed.
* **Set up the Home Shack "Sleep" Buff:** Add a timer-based speed or vision boost after using the bed.

### 🎒 Priority 2: Progression & Tools (Horizontal Growth)

* **Update the SpecialistObject Class:** Check if the player's `current_kit` matches the object (e.g., only the **Extractor** can mine **Rare Ore**).
* **Implement the Satchel Upgrade:** Limit active tools, forcing trips back to the village to swap kits.
* **Add "Tool" Visuals:** Update the UI to show which tool is currently active.

### 📜 Priority 3: Exploration Polish (Dungeon)

* **📈 Dynamic Dungeon Scaling:** Update the `DungeonGenerator` to increase the `width`, `height`, and `max_tiles` based on the player's total XP or "Pen" level.
* **Refine the Generator:** Add "Room" logic for open chambers connected by narrow halls.
* **Add the Evaluation State:** A summary screen showing Tiles Mapped, Loot Found, and Gold Salvaged.
* **Ink-Drain Balancing:** Fine-tune the drain rate to create "gentle pressure."

### 🎨 Priority 4: Visuals & UX

* **Map "Blueprint" Polish:** Add a grid-paper texture to the `fog_mask`.
* **Transition Fades:** Add black-to-alpha fades when switching between Town and Dungeon.
* **Tile Variance:** Use different textures for walls based on the dungeon type.

---

**Would you like me to show you how to modify the `Level` class to pass a "Scale Factor" to the `DungeonGenerator` so you can knock that new todo off the list first?**